# Supply Chain Analytics Toolkit

**Case study 01: Strategic sourcing using World Bank procurement awards**

This project started with a practical question: how can purchasing teams use contract data to identify categories that may require closer attention? I wanted to examine supplier concentration without assuming that a small number of suppliers necessarily indicates poor procurement performance.

The repository has two parts. The first is an empirical analysis of World Bank Group corporate procurement awards for FY2026. The second is a small set of reusable Python functions for data quality, procurement, supplier analysis, inventory classification, and hypothetical sourcing scenarios. Keeping these parts separate matters because not every dataset contains the same information. In particular, the World Bank records do not provide delivery dates or unit purchase prices.

## Main findings

The FY2026 data contains 713 award records, including 704 with disclosed positive values. These represent approximately USD 202.67 million in *published award values*, rather than actual payments. Contract Consultants and Consulting together account for about 77.8% of this disclosed amount. This makes them reasonable starting points for a category-level review, although their award sizes alone cannot establish overpayment or possible savings.

Audio Visual is a smaller category with a relatively high award-value concentration score (HHI approximately 3,043, based on 10 valued awards). This may justify further investigation, but the sample is small and the score is not evidence of poor supplier performance. See [the executive report](reports/executive_summary.md) for detailed calculations and qualifications.

## How to reproduce the case study

```bash
python -m pip install -r requirements.txt
python build_portfolio.py
python run_analysis.py
python -m unittest discover -s tests -v
```

The empirical notebook is at `notebooks/02_empirical_fy26_analysis.ipynb`. Figures and supporting tables are available in `figures/` and `outputs/`.

## Reusing the toolkit

The functions in `src/` accept column names as parameters. This means the same concentration calculation can be used with purchase orders, contract awards, or other datasets containing supplier identifiers and comparable monetary values. See `examples/reuse_with_another_dataset.py` for a starting point.

| Module | Purpose | Required information |
| --- | --- | --- |
| `data_quality.py` | Missingness and duplicate checks | Any DataFrame |
| `procurement.py` | Category-level value summaries | Category and monetary value |
| `suppliers.py` | Supplier concentration | Supplier and monetary value |
| `suppliers.py` | On-time delivery | Supplier, promised and actual dates |
| `inventory.py` | ABC classification | Item, annual units and unit cost |
| `scenarios.py` | Hypothetical supplier diversification | Observed supplier value shares |
| `visualizations.py` | Ranked bar charts | Aggregated numeric series |

The delivery and inventory functions are reusable tools, **not findings from the World Bank dataset**. They should only be applied when a future dataset contains the required variables.

## Data and limitations

Source: World Bank Group, *Corporate Procurement Contract Awards* (DS00028), downloaded 7 November 2026, CC BY 4.0. https://financesone.worldbank.org/d/DS00028

The data covers published awards above changing reporting thresholds, and some contract values are estimates. Supplier names are not fully reconciled to legal entities. The analysis therefore focuses on descriptive exposure and transparent what-if calculations, not on achieved savings, delivery reliability, or supplier quality. FY2026 is used as the main period to avoid crossing the reporting threshold change in Q3 FY2025.

This is an independent external case study, not an assessment of P&G suppliers. AI assistance was used in preparing the project; any personal portfolio claims should reflect the work the author can reproduce and explain.
