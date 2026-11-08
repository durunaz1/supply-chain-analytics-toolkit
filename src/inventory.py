"""Reusable inventory calculations, not applied to award-only data."""
import pandas as pd

def abc_classification(df, item, annual_units, unit_cost, a_cutoff=0.80, b_cutoff=0.95):
    """Classify items using observed annual usage value; assumes nonnegative inputs."""
    if not 0<a_cutoff<b_cutoff<1:
        raise ValueError('Cutoffs must satisfy 0 < A < B < 1')
    x=df[[item,annual_units,unit_cost]].dropna().copy()
    for c in [annual_units,unit_cost]:
        x[c]=pd.to_numeric(x[c],errors='raise')
        if (x[c]<0).any(): raise ValueError('Negative units or cost')
    x['annual_usage_value']=x[annual_units]*x[unit_cost]
    x=x.groupby(item,as_index=False).annual_usage_value.sum().sort_values('annual_usage_value',ascending=False)
    total=x.annual_usage_value.sum()
    if total<=0: raise ValueError('Total annual usage value must be positive')
    x['cumulative_share']=x.annual_usage_value.cumsum()/total
    previous=(x.annual_usage_value.cumsum()-x.annual_usage_value)/total
    x['abc_class']=previous.map(lambda v:'A' if v<a_cutoff else ('B' if v<b_cutoff else 'C'))
    return x
