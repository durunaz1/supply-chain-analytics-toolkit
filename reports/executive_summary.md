# Strategic Sourcing Intelligence | Executive Decision Brief

**Source:** World Bank Group Corporate Procurement Contract Awards, downloaded 7 November 2026; analysis of the complete World Bank fiscal year FY26 (1 July 2025–30 June 2026). Official data are not P&G procurement records.

## Decision in one minute

**Recommendation:** Do not initiate supplier replacement from award records alone. Establish a targeted category-level sourcing review, beginning with the two largest published categories, and request the missing information needed for a defensible procurement decision.

- **713 FY26 award records**, of which **704 have positive disclosed values** and **9 have missing award amounts** (1.3%).
- **USD 202.67 million** in disclosed FY26 award values (not paid spend).
- **CONTRACT CONSULTANTS** represents **81.69 million** (40.3%); **CONSULTING** represents **75.97 million** (37.5%). Together these represent **77.8%** of disclosed FY26 awards.
- Top ten named suppliers represent **12.9%** of FY26 disclosed award value across all categories; supplier aliases and legal ownership have not been fully resolved.

## Category screening (FY26)

| Category | Awards with values | Named suppliers | Award value (USD m) | Top supplier share | HHI |
|---|---:|---:|---:|---:|---:|
| CONTRACT CONSULTANTS | 234 | 212 | 81.69 | 3.6% | 122 |
| CONSULTING | 322 | 278 | 75.97 | 2.2% | 56 |
| EXTERNAL/CATERED EVENT | 66 | 57 | 14.75 | 7.8% | 296 |
| FINANCIAL SERVICES | 5 | 4 | 6.27 | 73.7% | 5,813 |
| TRANSPORTATION | 9 | 9 | 4.52 | 54.5% | 3,387 |
| AUDIO VISUAL | 10 | 7 | 4.36 | 42.4% | 3,043 |
| TRAINING | 11 | 10 | 3.78 | 42.6% | 2,311 |
| TELECOMMUNICATIONS | 16 | 14 | 2.62 | 18.1% | 942 |
| MEDICAL | 1 | 1 | 1.90 | 100.0% | 10,000 |

**Interpretation:** HHI is calculated from *published contract award value shares within the selected category and period*. It does not measure the suppliers' market shares, delivery reliability, substitutability, or probability of disruption. A category with very few awards can look highly concentrated for purely mechanical reasons.

## What-if sourcing stress test (not a forecast)

For the highest-HHI category with at least 10 disclosed awards and 3 named suppliers, **AUDIO VISUAL**, the observed FY26 award-value HHI is **3,043**. Hypothetically moving **20% of the largest supplier's recorded value to two entirely new equally sized suppliers** would change the arithmetic HHI to **2,431** (change **-611** points). This does **not** demonstrate feasible supplier capacity, cost savings, lower delivery risk, or ability to switch contracts.

## Three purchasing recommendations

1. **Prioritize high-value categories for category-manager review.** Start with CONTRACT CONSULTANTS and CONSULTING because they account for 77.8% of disclosed FY26 award value. Segment by service scope, organization, and contracting strategy before negotiating or consolidating.
2. **Build a supplier master-data and concentration control.** Resolve supplier aliases and parent-company relationships; then recalculate supplier share, top-3 dependence, and category HHI. Set review thresholds only after confirming legal entities and category definitions.
3. **Investigate the relatively concentrated AUDIO VISUAL category before considering diversification.** Obtain comparable supplier bids, scope specifications, service-level evidence, switching costs, and capacity limits. Use the published scenario table as a screening tool, not a claim of realized savings.

## Data-quality and inference caveats

- **500 of 4,799 records** in the complete source have missing award values; the analysis does not impute them.
- The disclosure threshold changed from USD 250,000 to USD 100,000 in Q3 FY25. We analyze the complete FY26 period to avoid mixing these two thresholds within the primary results. This is a published-award sample, not all procurement activity.
- Some IDIQ contract values are estimates. Published awards are not actual expenditures, invoice prices, quantities, margins, or procurement savings.
- FY26 contains **30 repeated non-null selection numbers**. They are retained because repeated identifiers do not establish duplicate award rows. Investigate contract line granularity before any contract-count claim.
- Supplier country reflects vendor registration, not proven production location. No delivery dates, lead times, quality measures, supplier capacities, or realized prices exist in this dataset.
- Contract scope and duration are not standardized; differences in award size must **not** be interpreted as price inefficiency.
- This is an **external procurement benchmark** demonstrating analytical methods, not an assessment of P&G's actual suppliers.

## Decision gate for Purchasing Manager

**Approve a 2–4 week supplier/category data-enrichment review, not a supplier switch.** Success means identifying comparable service groups, verified supplier entities, measurable service performance, and qualified sourcing alternatives. Any future savings business case must use real bids and a total-cost model.

## Reproducibility

Run `python build_portfolio.py` and `python run_analysis.py` from the project root. Outputs include five figures, category and supplier CSV tables, outlier sensitivity, and scenario results. See `notebooks/02_empirical_fy26_analysis.ipynb` for an interactive walkthrough.
