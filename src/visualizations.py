"""Simple reusable chart function; caller owns saving and labeling."""
import matplotlib.pyplot as plt

def ranked_values(series, title, xlabel='Observed value', top_n=12):
    ax=series.nlargest(top_n).sort_values().plot.barh(figsize=(9,5))
    ax.set_title(title);ax.set_xlabel(xlabel)
    ax.figure.tight_layout()
    return ax
