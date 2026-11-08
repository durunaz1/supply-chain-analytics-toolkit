"""Reusable, data-independent sourcing concentration functions."""
import numpy as np
import pandas as pd


def supplier_concentration(df, supplier='supplier', value='award_value'):
    """Compute award-value supplier concentration; requires nonnegative values."""
    x = df[[supplier, value]].dropna().copy()
    if (x[value] < 0).any():
        raise ValueError('Negative award values require separate treatment.')
    totals = x.groupby(supplier, dropna=False)[value].sum().sort_values(ascending=False)
    total = totals.sum()
    if total <= 0:
        raise ValueError('No positive award value available.')
    shares = totals / total
    return {'supplier_count': len(shares), 'total_awarded': float(total),
            'top_1_share': float(shares.iloc[:1].sum()),
            'top_5_share': float(shares.iloc[:5].sum()),
            'hhi': float((shares ** 2).sum()),
            'supplier_shares': shares}


def hypothetical_diversification(shares, moved_fraction=0.10, new_supplier_count=1):
    """Illustrative redistribution of largest supplier's share, not an achievable forecast."""
    if not 0 <= moved_fraction <= 1 or new_supplier_count < 1:
        raise ValueError('Invalid scenario assumptions.')
    s = pd.Series(shares, dtype=float).copy()
    if s.empty or (s < 0).any() or not np.isclose(s.sum(), 1):
        raise ValueError('Input shares must be nonnegative and sum to one.')
    largest = s.idxmax()
    moved = s[largest] * moved_fraction
    s[largest] -= moved
    for i in range(new_supplier_count):
        name = f'__hypothetical_new_supplier_{i+1}__'
        if name in s.index:
            raise ValueError('Scenario supplier name collision.')
        s.loc[name] = moved / new_supplier_count
    return {'baseline_hhi': float((pd.Series(shares) ** 2).sum()),
            'scenario_hhi': float((s ** 2).sum()), 'scenario_shares': s}
