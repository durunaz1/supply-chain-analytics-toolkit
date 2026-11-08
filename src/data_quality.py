"""Basic quality checks that work across datasets."""
import pandas as pd

def audit(df, required=(), key=None):
    """Return a transparent data-quality summary without modifying the input."""
    missing = sorted(set(required).difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return {"rows": int(len(df)), "columns": int(len(df.columns)),
            "missing_by_column": {str(k): int(v) for k,v in df.isna().sum().items()},
            "duplicate_rows": int(df.duplicated().sum()),
            "repeated_keys": None if key is None else int(df[key].dropna().duplicated().sum())}
