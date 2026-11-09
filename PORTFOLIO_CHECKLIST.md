# Portfolio release checklist

## Verified locally (9 November 2026)
- [x] Original World Bank CSV included in data/raw/.
- [x] `python build_portfolio.py` completed.
- [x] `python run_analysis.py` completed.
- [x] `python -m unittest discover -s tests -v`: 8 tests passed.
- [x] README includes findings, figures, data source, and limitations.
- [x] Executive analysis is linked from README.

## Verify after publishing to GitHub
- [ ] README images render correctly on the repository home page.
- [ ] `reports/executive_summary.md` is the updated version.
- [ ] The notebook opens and its figures/results are readable.
- [ ] Reproduce the environment using README instructions on another computer.
- [ ] Personally review and explain the analysis before claiming independent development.

## Data caveats to retain
- Published award values are not realized expenditure or unit prices.
- Missing award values are excluded from value-weighted metrics, not replaced with zero.
- Repeated selection numbers are flagged; they are not automatically removed because record granularity is uncertain.
- Supplier names are not verified legal-entity identifiers.
- Diversification is hypothetical and does not demonstrate feasible savings.
