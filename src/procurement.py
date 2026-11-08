"""General procurement calculations; values must be comparable."""
import pandas as pd

def category_value(df, category, value):
    """Aggregate observed monetary values; missing values are excluded, not set to zero."""
    if not {category,value}.issubset(df.columns):
        raise ValueError("Required columns are missing")
    x=df[[category,value]].copy()
    x[value]=pd.to_numeric(x[value],errors="coerce")
    if (x[value].dropna()<0).any():
        raise ValueError("Negative values require explicit treatment")
    return (x.dropna().groupby(category)[value].agg(['sum','count'])
            .rename(columns={'sum':'observed_value','count':'valued_records'})
            .sort_values('observed_value',ascending=False))
