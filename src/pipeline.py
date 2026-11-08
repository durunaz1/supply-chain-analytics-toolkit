"""Auditable procurement award analysis. No invented supplier or performance fields."""
from pathlib import Path
import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ALIASES = {
 'supplier':['supplier','vendor_name','vendor name'],
 'category':['commodity_category','commodity category'],
 'award_value':['contract_award_amount','contract award amount (usd)','amount','award_value'],
 'award_date':['award_date','award date'],
 'selection_number':['selection_number','selection number'],
 'organization':['wbg_organization','wbg organization','organisation'],
 'country':['supplier_country','supplier country / economy','vendor_country'],
}
def canonical(s):return re.sub(r'[^a-z0-9]+',' ',str(s).strip().lower()).strip()
def load_awards(path):
    raw=pd.read_csv(path,low_memory=False)
    names={canonical(c):c for c in raw.columns}
    mapped={}
    for target,options in ALIASES.items():
        for alias in options:
            if canonical(alias) in names:
                mapped[names[canonical(alias)]]=target;break
    required={'supplier','category','award_value','award_date'}
    if not required.issubset(mapped.values()):
        raise ValueError(f'Missing required fields: {sorted(required-set(mapped.values()))}. Available: {list(raw.columns)}')
    d=raw.rename(columns=mapped).copy()
    d['award_value']=pd.to_numeric(d['award_value'].astype(str).str.replace(',','',regex=False).str.replace('$','',regex=False),errors='coerce')
    d['award_date']=pd.to_datetime(d['award_date'],errors='coerce')
    for c in ['supplier','category']:
        d[c]=d[c].astype('string').str.strip().replace('',pd.NA)
    d['year']=d['award_date'].dt.year
    quality={
      'rows_raw':int(len(d)),
      'missing_supplier':int(d.supplier.isna().sum()),
      'missing_category':int(d.category.isna().sum()),
      'missing_award_value':int(d.award_value.isna().sum()),
      'missing_award_date':int(d.award_date.isna().sum()),
      'nonpositive_award_value':int((d.award_value<=0).fillna(False).sum()),
      'duplicate_selection_numbers':int(d['selection_number'].dropna().duplicated().sum()) if 'selection_number' in d else None,
      'note':'Repeated selection numbers are flagged, not automatically dropped: award line granularity must be investigated.'
    }
    good=d.dropna(subset=['supplier','category','award_value','award_date']).loc[lambda x:x.award_value>0].copy()
    quality['rows_usable']=int(len(good));quality['rows_excluded']=int(len(d)-len(good))
    if good.empty:raise ValueError('No usable award records')
    return good,quality

def category_metrics(df,min_awards=5):
    records=[]
    for (year,category),g in df.groupby(['year','category'],dropna=False):
        spend=g.groupby('supplier').award_value.sum()
        shares=spend/spend.sum()
        records.append({'year':int(year),'category':str(category),'awards':len(g),
                        'suppliers':len(spend),'awarded_usd':float(spend.sum()),
                        'top1_share':float(shares.max()),'top3_share':float(shares.nlargest(3).sum()),
                        'hhi_10000':float((shares.pow(2).sum())*10000),
                        'median_award_usd':float(g.award_value.median()),
                        'eligible_for_comparison':bool(len(g)>=min_awards and len(spend)>=2)})
    return pd.DataFrame(records).sort_values(['year','awarded_usd'],ascending=[False,False])

def sensitivity(shares, fractions=(0.05,0.10,0.20), new_counts=(1,2,3)):
    """Assumes fraction of largest supplier's value moved to hypothetical new vendors."""
    s=pd.Series(shares,dtype=float)
    if s.empty or (s<0).any() or not np.isclose(s.sum(),1):raise ValueError('Invalid shares')
    base=float((s*s).sum()*10000)
    rows=[]
    for f in fractions:
        for n in new_counts:
            t=s.copy();idx=t.idxmax();moved=t.loc[idx]*f;t.loc[idx]-=moved
            for i in range(n):t.loc[f'__new_{i}__']=moved/n
            h=float((t*t).sum()*10000)
            rows.append({'fraction_of_largest_supplier_reallocated':f,'new_suppliers':n,
                         'baseline_hhi':base,'scenario_hhi':h,'hhi_change':h-base,
                         'warning':'Counterfactual exposure only; no cost, capacity, reliability, or feasibility evidence'})
    return pd.DataFrame(rows)

def run(source,output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    figdir=out/'figures';figdir.mkdir(exist_ok=True)
    d,q=load_awards(source)
    q['source_file']=str(source)
    q['min_date']=str(d.award_date.min().date());q['max_date']=str(d.award_date.max().date())
    (out/'data_quality.json').write_text(json.dumps(q,indent=2))
    cats=category_metrics(d);cats.to_csv(out/'category_year_metrics.csv',index=False)
    suppliers=d.groupby('supplier').agg(awarded_usd=('award_value','sum'),award_count=('award_value','size')).sort_values('awarded_usd',ascending=False)
    suppliers.to_csv(out/'supplier_awards.csv')
    annual=d.groupby('year').award_value.agg(['sum','size']);annual.to_csv(out/'annual_awards.csv')
    latest=int(d.year.max())
    eligible=cats[(cats.year==latest)&cats.eligible_for_comparison].sort_values('awarded_usd',ascending=False)
    if not eligible.empty:
        chosen=eligible.iloc[0]['category']
        sub=d[(d.year==latest)&(d.category==chosen)]
        shares=sub.groupby('supplier').award_value.sum();shares=shares/shares.sum()
        sensitivity(shares).to_csv(out/'diversification_sensitivity.csv',index=False)
    else:chosen=None
    plt.figure(figsize=(9,4));annual['sum'].plot.bar();plt.title('Published contract award value by calendar year');plt.ylabel('Awarded USD (not spend paid)');plt.tight_layout();plt.savefig(figdir/'annual_awards.png',dpi=160);plt.close()
    top=d.groupby('category').award_value.sum().nlargest(12).sort_values()
    plt.figure(figsize=(9,6));top.plot.barh();plt.title('Largest commodity categories by published award value');plt.xlabel('Awarded USD');plt.tight_layout();plt.savefig(figdir/'category_awards.png',dpi=160);plt.close()
    sample=cats[cats.eligible_for_comparison]
    if not sample.empty:
        plt.figure(figsize=(9,5));plt.scatter(sample.awarded_usd,sample.hhi_10000,alpha=.6)
        plt.xscale('log');plt.xlabel('Category-year awarded USD (log scale)');plt.ylabel('Supplier HHI (0–10,000)');plt.title('Concentration versus published award value');plt.tight_layout();plt.savefig(figdir/'concentration_map.png',dpi=160);plt.close()
    report=f'''# Strategic sourcing intelligence — evidence brief\n\nSource: World Bank Group corporate procurement award CSV.\n\n## Verified descriptive coverage\n- Usable award records: {len(d):,} of {q['rows_raw']:,}\n- Calendar-year range: {q['min_date']} to {q['max_date']}\n- Published award value in usable records: USD {d.award_value.sum():,.0f}\n- Distinct named suppliers (not consolidated corporate groups): {d.supplier.nunique():,}\n- Distinct commodity categories: {d.category.nunique():,}\n- Latest observed calendar year: {latest}\n\n## Decision screening\n- Largest eligible category by awarded value in latest year: {chosen or 'None meets minimum coverage criteria'}\n- HHI measures concentration of **published award values**, not market concentration or disruption probability.\n- Supplier reallocation scenarios are mathematical counterfactuals, **not feasible procurement plans or savings estimates**.\n\n## Recommended diligence before any sourcing action\n1. Confirm supplier legal entities and corporate relationships; aliases can bias concentration.\n2. Verify whether award scopes, contract terms and categories are genuinely comparable.\n3. Obtain supplier capacity, delivery service levels, qualification, and unit-price quotes before recommending a switch.\n\n## Material limitations\n- Published awards exclude smaller contracts and the reporting threshold changes over time; trends are not a complete spend series.\n- Some award values are estimates for indefinite-delivery contracts, not actual payments.\n- No unit quantities, realized prices, lead times, delivery outcomes, or actual savings are provided.\n- No causal inference about supplier selection or diversification is possible.\n'''
    (out/'evidence_brief.md').write_text(report)
    return q
