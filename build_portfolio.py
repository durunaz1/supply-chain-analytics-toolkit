"""Generate empirical decision brief, charts and reproducible notebook from real World Bank award records."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat as nbf
from src.pipeline import load_awards, sensitivity
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
RAW=ROOT/'data/raw/world_bank_awards.csv'
raw=pd.read_csv(RAW); raw['date']=pd.to_datetime(raw['Award Date'],format='%m/%d/%Y')
raw['value']=pd.to_numeric(raw['Contract Award Amount (USD)'],errors='coerce')
raw['supplier_clean']=raw['Supplier'].astype(str).str.strip().str.casefold().str.replace(r'\s+',' ',regex=True)
fy=raw.loc[raw.date.between('2025-07-01','2026-06-30')].copy()
valid=fy.loc[fy.value.notna()&(fy.value>0)].copy()
category=valid.groupby('Commodity Category').agg(awards=('value','size'),awarded_usd=('value','sum'),suppliers=('supplier_clean','nunique'),median_award=('value','median')).sort_values('awarded_usd',ascending=False)
category['share']=category.awarded_usd/category.awarded_usd.sum()
rows=[]
for cat,g in valid.groupby('Commodity Category'):
 s=g.groupby('supplier_clean').value.sum().sort_values(ascending=False); share=s/s.sum()
 rows.append(dict(category=cat,awards=len(g),suppliers=len(s),awarded_usd=s.sum(),top1_share=share.iloc[0],top3_share=share.head(3).sum(),hhi=10000*(share**2).sum(),top_supplier=g.groupby('supplier_clean').value.sum().idxmax()))
metrics=pd.DataFrame(rows).sort_values('awarded_usd',ascending=False)
metrics.to_csv(OUT/'fy26_category_risk.csv',index=False)
valid.groupby('supplier_clean').agg(awards=('value','size'),awarded_usd=('value','sum')).sort_values('awarded_usd',ascending=False).to_csv(OUT/'fy26_supplier_awards.csv')
category.to_csv(OUT/'fy26_category_awards.csv')
quality=pd.DataFrame({'metric':['total_rows','fy26_rows','fy26_valued_rows','fy26_missing_amount','all_period_missing_amount','all_period_duplicate_selection_numbers_nonnull','fy26_duplicate_selection_numbers_nonnull','fy26_distinct_supplier_names','fy26_awarded_value_usd'], 'value':[len(raw),len(fy),len(valid),fy.value.isna().sum(),raw.value.isna().sum(),raw['Selection Number'].dropna().duplicated().sum(),fy['Selection Number'].dropna().duplicated().sum(),valid.supplier_clean.nunique(),valid.value.sum()]})
quality.to_csv(OUT/'audit_summary.csv',index=False)
# A concentration counterfactual for the largest eligible category, not a savings model.
chosen=metrics.query('awards >= 10 and suppliers >= 3').sort_values('hhi',ascending=False).iloc[0]
sub=valid[valid['Commodity Category']==chosen.category]
s=sub.groupby('supplier_clean').value.sum();scenario=sensitivity(s/s.sum(),fractions=(.1,.2,.3),new_counts=(1,2,3));scenario.to_csv(OUT/'fy26_diversification_scenarios.csv',index=False)
# concentration sensitivity to largest award (one contract)
large=valid.loc[valid.value.idxmax()]
without=valid.drop(index=valid.value.idxmax())
def hhi(g):
 v=g.groupby('supplier_clean').value.sum();return float(((v/v.sum())**2).sum()*10000)
robust=pd.DataFrame([{'scope':'FY26 all categories','hhi_all':hhi(valid),'hhi_without_largest_award':hhi(without),'largest_award_usd':large.value,'largest_award_category':large['Commodity Category']}, {'scope':str(chosen.category),'hhi_all':hhi(sub),'hhi_without_largest_award':hhi(sub.drop(index=sub.value.idxmax())),'largest_award_usd':sub.value.max(),'largest_award_category':chosen.category}]);robust.to_csv(OUT/'outlier_sensitivity.csv',index=False)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def save(name):plt.tight_layout();plt.savefig(FIG/name,dpi=180,bbox_inches='tight');plt.close()
ax=category.head(10).sort_values('awarded_usd').awarded_usd.div(1e6).plot.barh(figsize=(10,5.5),color='#164e63');ax.set_xlabel('Disclosed FY26 award value (USD millions)');ax.set_ylabel('');ax.set_title('Where published FY26 contract value is concentrated');save('01_fy26_category_value.png')
plot=metrics.query('awards >= 10 and suppliers >= 3').copy()
fig,ax=plt.subplots(figsize=(11,6.5))
ax.scatter(plot.awarded_usd/1e6,plot.hhi,s=plot.awards*3,alpha=.72,c='#0f766e')
ax.set_xscale('log')
ax.set_xticks([2,5,10,20,50,100])
ax.set_xticklabels(['2','5','10','20','50','100'])
ax.set_xlim(1.5,140)
ax.set_ylim(-260,4000)
ax.set_xlabel('FY26 disclosed award value (USD millions, log scale)')
ax.set_ylabel('Award-value HHI (0–10,000)')
ax.set_title('Procurement category size and supplier dependence are different')
for threshold in (1500,2500):
 ax.axhline(threshold,color='#64748b',linestyle='--',linewidth=.8,alpha=.65)
 ax.text(135,threshold+40,f'{threshold:,} reference',ha='right',fontsize=8,color='#475569')
# Historical market-concentration reference lines are illustrative, not procurement-risk thresholds.
labels={
 'CONTRACT CONSULTANTS':(5,16),
 'CONSULTING':(5,-16),
 'EXTERNAL/CATERED EVENT':(7,8),
 'AUDIO VISUAL':(8,8),
 'TRAINING':(7,-14),
 'TELECOMMUNICATIONS':(8,10),
}
for _,r in plot.iterrows():
 if r.category in labels:
  ax.annotate(r.category.title(),(r.awarded_usd/1e6,r.hhi),xytext=labels[r.category],textcoords='offset points',fontsize=8)
save('02_fy26_concentration_map.png')
fig,ax=plt.subplots(figsize=(9,4.5));sns=sub.groupby('supplier_clean').value.sum().sort_values(ascending=False);top=sns.head(12);ax.bar(range(1,len(top)+1),top.values/1e6,color='#164e63');ax.set_xlabel('Supplier rank in '+str(chosen.category));ax.set_ylabel('Award value (USD millions)');ax.set_title('Top supplier exposure within largest eligible category');save('03_supplier_exposure.png')
fig,ax=plt.subplots(figsize=(8,4.5));forplot=scenario.pivot(index='fraction_of_largest_supplier_reallocated',columns='new_suppliers',values='scenario_hhi');forplot.plot(marker='o',ax=ax);ax.axhline(scenario.baseline_hhi.iloc[0],ls='--',color='gray',label='Baseline');ax.set_xlabel('Share of top supplier awards hypothetically reallocated');ax.set_ylabel('Counterfactual HHI');ax.set_title('Diversification reduces arithmetic concentration, not proven risk');save('04_scenario_sensitivity.png')
fig,ax=plt.subplots(figsize=(9,4.5));m=raw.assign(year=raw.date.dt.year,missing=raw.value.isna()).groupby('year').missing.mean()*100;m.plot.bar(ax=ax,color='#a16207');ax.set_ylabel('Records without disclosed value (%)');ax.set_xlabel('Calendar year');ax.set_title('Award-value disclosure varies over time');save('05_missingness.png')
amount=valid.value.sum();top2=category.head(2).awarded_usd.sum()/amount;top10=valid.groupby('supplier_clean').value.sum().nlargest(10).sum()/amount
c1=metrics.iloc[0]; c2=metrics.iloc[1];base=scenario.baseline_hhi.iloc[0];case=scenario.query('fraction_of_largest_supplier_reallocated == 0.2 and new_suppliers == 2').iloc[0]
summary=f'''# Strategic Sourcing Intelligence | Executive Decision Brief

**Source:** World Bank Group Corporate Procurement Contract Awards, downloaded 7 November 2026; analysis of the complete World Bank fiscal year FY26 (1 July 2025–30 June 2026). This is an external case study using public data, not internal company procurement records.

## Decision in one minute

**Recommendation:** Treat award value and supplier concentration as separate screening dimensions. Review high-value service categories for contract scope and category management; investigate concentrated smaller categories before considering any supplier changes.

- **{len(fy):,} FY26 award records**, of which **{len(valid):,} have positive disclosed values** and **{fy.value.isna().sum():,} have missing award amounts** ({fy.value.isna().mean():.1%}).
- **USD {amount/1e6:,.2f} million** in disclosed FY26 award values (not paid spend).
- **{category.index[0]}** represents **{c1.awarded_usd/1e6:,.2f} million** ({c1.awarded_usd/amount:.1%}); **{category.index[1]}** represents **{c2.awarded_usd/1e6:,.2f} million** ({c2.awarded_usd/amount:.1%}). Together these represent **{top2:.1%}** of disclosed FY26 awards.
- Top ten named suppliers represent **{top10:.1%}** of FY26 disclosed award value across all categories; supplier aliases and legal ownership have not been fully resolved.

## Category screening (FY26)

| Category | Awards with values | Named suppliers | Award value (USD m) | Top supplier share | HHI |
|---|---:|---:|---:|---:|---:|
'''
for _,r in metrics.head(9).iterrows():summary+=f'| {r.category} | {r.awards:,} | {r.suppliers:,} | {r.awarded_usd/1e6:,.2f} | {r.top1_share:.1%} | {r.hhi:,.0f} |\n'
summary+=f'''
**Interpretation:** HHI is calculated from *published contract award value shares within the selected category and period*. It does not measure the suppliers' market shares, delivery reliability, substitutability, or probability of disruption. A category with very few awards can look highly concentrated for purely mechanical reasons.

## What-if sourcing stress test (not a forecast)

For the highest-HHI category with at least 10 disclosed awards and 3 named suppliers, **{chosen.category}**, the observed FY26 award-value HHI is **{base:,.0f}**. Hypothetically moving **20% of the largest supplier's recorded value to two entirely new equally sized suppliers** would change the arithmetic HHI to **{case.scenario_hhi:,.0f}** (change **{case.hhi_change:,.0f}** points). This does **not** demonstrate feasible supplier capacity, cost savings, lower delivery risk, or ability to switch contracts.

**Additional category observation:** Financial Services has only five valued awards, so its high HHI is a small-sample screening signal. The Medical category has one award and HHI 10,000 by construction. The scenario therefore requires at least ten valued awards and three named suppliers.

## Three purchasing recommendations

1. **Review high-value service categories for scope and contract management, not assumed concentration risk.** Start with {category.index[0]} and {category.index[1]} because they account for {top2:.1%} of disclosed FY26 award value. Segment by service scope, organization, and contracting strategy before negotiating or consolidating.
2. **Build a supplier master-data and concentration control.** Resolve supplier aliases and parent-company relationships; then recalculate supplier share, top-3 dependence, and category HHI. Set review thresholds only after confirming legal entities and category definitions.
3. **Investigate the relatively concentrated {chosen.category} category before considering diversification.** Obtain comparable supplier bids, scope specifications, service-level evidence, switching costs, and capacity limits. Use the published scenario table as a screening tool, not a claim of realized savings.

## Data-quality and inference caveats

- **{raw.value.isna().sum():,} of {len(raw):,} records** in the complete source have missing award values; the analysis does not impute them.
- The disclosure threshold changed from USD 250,000 to USD 100,000 in Q3 FY25. We analyze the complete FY26 period to avoid mixing these two thresholds within the primary results. This is a published-award sample, not all procurement activity.
- Some IDIQ contract values are estimates. Published awards are not actual expenditures, invoice prices, quantities, margins, or procurement savings.
- FY26 contains **{fy['Selection Number'].dropna().duplicated().sum():,} repeated non-null selection numbers**. They are retained because repeated identifiers do not establish duplicate award rows. Investigate contract line granularity before any contract-count claim.
- Supplier country reflects vendor registration, not proven production location. No delivery dates, lead times, quality measures, supplier capacities, or realized prices exist in this dataset.
- Contract scope and duration are not standardized; differences in award size must **not** be interpreted as price inefficiency.
- This is an **external procurement case study**, not an assessment of any company's internal suppliers.

## Decision gate for Purchasing Manager

**Approve a 2–4 week supplier/category data-enrichment review, not a supplier switch.** Success means identifying comparable service groups, verified supplier entities, measurable service performance, and qualified sourcing alternatives. Any future savings business case must use real bids and a total-cost model.

## Reproducibility

Run `python build_portfolio.py` and `python run_analysis.py` from the project root. Outputs include five figures, category and supplier CSV tables, outlier sensitivity, and scenario results. See `notebooks/02_empirical_fy26_analysis.ipynb` for an interactive walkthrough.
'''
(ROOT/'reports'/'executive_summary.md').write_text(summary)
# notebook designed for independent execution and business interpretation
cells=[
 nbf.v4.new_markdown_cell('# Strategic Sourcing Intelligence — FY26 empirical analysis\nReal World Bank procurement award data. **Awards are not actual spend, unit prices or delivery performance.**'),
 nbf.v4.new_code_cell('from pathlib import Path\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom src.pipeline import sensitivity\nROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()\ndf = pd.read_csv(ROOT / "data/raw/world_bank_awards.csv")\ndf.shape'),
 nbf.v4.new_markdown_cell('## 1. Audit schema and missingness\nMissing values are not zero. Repeated selection numbers are not automatically duplicate contracts.'),
 nbf.v4.new_code_cell('display(df.isna().sum().to_frame("missing"))\nprint("Exact duplicate rows:", df.duplicated().sum())\nprint("Repeated non-null selection numbers:", df["Selection Number"].dropna().duplicated().sum())'),
 nbf.v4.new_markdown_cell('## 2. Focus on the complete FY26 disclosure regime\nThe published reporting threshold changed in Q3 FY25. FY26 is July 2025 through June 2026.'),
 nbf.v4.new_code_cell('df["date"] = pd.to_datetime(df["Award Date"], format="%m/%d/%Y")\ndf["value"] = pd.to_numeric(df["Contract Award Amount (USD)"], errors="coerce")\ndf["supplier_clean"] = df["Supplier"].str.strip().str.casefold().str.replace(r"\\s+", " ", regex=True)\nfy = df[df.date.between("2025-07-01", "2026-06-30")].copy()\nvalid = fy[fy.value.notna() & fy.value.gt(0)].copy()\nprint("FY26 rows:",len(fy),"usable:",len(valid),"missing amounts:",fy.value.isna().sum())'),
 nbf.v4.new_markdown_cell('## 3. Category exposure\nRank categories by published award value. These are **not** comparable unit prices.'),
 nbf.v4.new_code_cell('category = valid.groupby("Commodity Category").agg(awards=("value","size"),awarded_usd=("value","sum"),suppliers=("supplier_clean","nunique")).sort_values("awarded_usd",ascending=False)\ncategory["share"] = category.awarded_usd / category.awarded_usd.sum()\ndisplay(category.head(12))\ncategory.head(10).awarded_usd.sort_values().div(1e6).plot.barh(figsize=(9,5),title="FY26 disclosed award value by category (USD m)"); plt.show()'),
 nbf.v4.new_markdown_cell('## 4. Supplier concentration\nHHI = 10,000 × sum of squared supplier award-value shares. High HHI is a screening flag, not evidence of supplier failure.'),
 nbf.v4.new_code_cell('rows=[]\nfor cat,g in valid.groupby("Commodity Category"):\n    values=g.groupby("supplier_clean").value.sum()\n    shares=values/values.sum()\n    rows.append({"category":cat,"awards":len(g),"suppliers":len(values),"awarded_usd":values.sum(),"top1_share":shares.max(),"hhi":10000*(shares**2).sum()})\nmetrics=pd.DataFrame(rows).sort_values("awarded_usd",ascending=False)\ndisplay(metrics.head(12))'),
 nbf.v4.new_markdown_cell('## 5. Decision scenario, not an optimization claim\nReallocate part of the top supplier’s award value to hypothetical new suppliers. This does not establish feasibility or cost savings.'),
 nbf.v4.new_code_cell('chosen=metrics.query("awards >= 10 and suppliers >= 3").sort_values("hhi",ascending=False).iloc[0].category\ns=valid.loc[valid["Commodity Category"].eq(chosen)].groupby("supplier_clean").value.sum()\nscenarios=sensitivity(s/s.sum(),fractions=(.1,.2,.3),new_counts=(1,2,3))\nprint("Category:",chosen)\ndisplay(scenarios)'),
 nbf.v4.new_markdown_cell('## 6. Manager challenge\nWhat evidence would you require before proposing a real supplier switch? Consider scope comparability, supplier capacity, service levels, switching costs, contract restrictions, and qualification risk.\n\n**Limitations:** No delivery timestamps, quantity/unit prices, realized savings, supplier capacities, or reliable corporate-parent IDs. A lower HHI is not proof of lower operational risk.'),
]
nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
nbf.write(nb,ROOT/'notebooks'/'02_empirical_fy26_analysis.ipynb')
print('FY26',len(fy),len(valid),'USD',amount,'top2',top2,'chosen',chosen,'scenario',base,case.scenario_hhi)
