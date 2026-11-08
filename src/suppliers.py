"""Supplier metrics; distinguish award exposure from supplier reliability."""
import numpy as np
import pandas as pd

def concentration(df, supplier, value, scale=10000):
    """Compute concentration in observed value (not supplier market share)."""
    if not {supplier,value}.issubset(df.columns):
        raise ValueError("Required columns are missing")
    x=df[[supplier,value]].dropna().copy()
    x[value]=pd.to_numeric(x[value],errors='raise')
    if (x[value]<0).any():
        raise ValueError('Negative values are not supported')
    totals=x.groupby(supplier)[value].sum()
    totals=totals[totals>0].sort_values(ascending=False)
    if totals.empty:
        raise ValueError('No positive supplier value')
    shares=totals/totals.sum()
    return {'total_value':float(totals.sum()),'supplier_count':int(len(shares)),
            'top1_share':float(shares.iloc[0]),'top3_share':float(shares.iloc[:3].sum()),
            'hhi':float(scale*(shares**2).sum()),'shares':shares}

def on_time_delivery(df, promised_date, actual_date, supplier):
    """On-time delivery rate; requires real promised and actual delivery timestamps."""
    if not {promised_date,actual_date,supplier}.issubset(df.columns):
        raise ValueError('Actual and promised delivery dates are required; cannot infer reliability from awards')
    x=df[[promised_date,actual_date,supplier]].copy()
    x[promised_date]=pd.to_datetime(x[promised_date],errors='coerce')
    x[actual_date]=pd.to_datetime(x[actual_date],errors='coerce')
    x=x.dropna()
    if x.empty:
        raise ValueError('No valid delivery date pairs')
    x['on_time']=x[actual_date]<=x[promised_date]
    return x.groupby(supplier).on_time.agg(['mean','size']).rename(columns={'mean':'on_time_rate','size':'observed_deliveries'})
