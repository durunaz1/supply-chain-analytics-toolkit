# Strategic Sourcing Intelligence — World Bank FY26 Procurement Awards

A reproducible, **real-data** purchasing decision-support case study, developed as an external procurement benchmark relevant to sourcing analytics. Not P&G internal data.

## Key output

Read [`reports/executive_summary.md`](reports/executive_summary.md) for verified findings and evidence-based recommendations. See `figures/` for charts, `outputs/` for machine-readable tables and `notebooks/02_empirical_fy26_analysis.ipynb` for the executable notebook.

## Source and attribution

World Bank Group, *Corporate Procurement Contract Awards* (DS00028), downloaded 7 November 2026, CC BY 4.0. https://financesone.worldbank.org/d/DS00028

## Reproduce

```bash
pip install -r requirements.txt
python build_portfolio.py
python run_analysis.py
python -m unittest discover -s tests -v
```

The official source CSV is stored at `data/raw/world_bank_awards.csv`. The primary analysis uses FY26 (July 2025–June 2026), avoiding the reporting-threshold change that occurred in Q3 FY25. The historical pipeline provides exploratory diagnostics only and **must not** be used to claim spend growth.

## Method

Disclosed award values, missingness, supplier/category concentration (top-1, top-3, HHI), outlier sensitivity, and hypothetical supplier diversification. No delivery, unit prices, supplier capacity, or realized savings data exist. A reduction in modeled HHI does not establish a feasible or beneficial sourcing action.

## Repository

- `data/raw/` source CSV (public data, CC BY 4.0)
- `src/` reusable analysis functions
- `notebooks/` guided and empirical notebooks
- `build_portfolio.py` verified analysis, charts, decision report
- `figures/` exported visualizations
- `outputs/` auditable metrics
- `reports/` executive decision brief
- `tests/` unit tests

## Responsible representation

This portfolio was prepared with AI assistance. Present it as independently completed only if you personally reproduce, understand, validate and can defend the analysis. Do not claim verified supplier savings, delivery performance or P&G-specific findings.
