
# Strategic Sourcing Intelligence
### Supplier Concentration and Procurement Risk: A World Bank Case Study

## Introduction

Procurement decisions are not only about reducing costs. Organizations also need to consider how their purchasing activities are distributed across suppliers and whether depending on a small number of suppliers creates potential risks.

For example, working with fewer suppliers may simplify procurement processes and provide opportunities for negotiation. However, it can also increase dependence on individual suppliers. This means that evaluating procurement performance requires looking beyond total expenditure.

This project examines how real procurement data can be used to identify supplier concentration, understand purchasing patterns, and evaluate possible sourcing decisions.

The analysis uses publicly available World Bank Group procurement contract awards for fiscal year 2026. It is an external procurement case study, not an analysis of P&G's internal purchasing activities.

## Research Question

How can procurement data help identify supplier concentration and support sourcing decisions while accounting for potential supply risks?

## Dataset

**Source:** World Bank Group — Corporate Procurement Contract Awards (DS00028)

**Period:** FY2026 (July 2025 – June 2026)

**Source:** https://financesone.worldbank.org/d/DS00028

The dataset includes contract award values, suppliers, commodity categories, and award dates.

The analysis focuses on FY2026 because the reporting threshold changed during FY2025, making comparisons across earlier periods less straightforward.

## Methodology

The project uses Python, pandas, NumPy, and Matplotlib to examine procurement patterns.

The analysis includes:

1. Data cleaning and missing-value assessment.
2. Procurement award-value distribution across categories.
3. Supplier concentration analysis using top-supplier shares and the Herfindahl-Hirschman Index (HHI).
4. Supplier exposure and outlier sensitivity.
5. Hypothetical supplier diversification scenarios.

HHI is used to measure how concentrated award values are among suppliers within a category. A higher HHI indicates that a larger proportion of disclosed award value is associated with fewer suppliers.

However, concentration alone does not necessarily indicate poor procurement performance. Some categories may naturally require specialized suppliers, while others may benefit from a more diversified supplier base.

## Results and Visualizations

### 1. Procurement Award Values by Category

![Procurement Award Values](figures/01_fy26_category_value.png)

The analysis examines how disclosed contract award values are distributed across procurement categories.

In FY2026, Consulting and Contract Consultants together accounted for approximately 77.8% of disclosed award value. This suggests that these categories may deserve particular attention when evaluating procurement exposure.

However, a large award-value share does not necessarily indicate inefficiency or excessive spending.

### 2. Supplier Concentration

![Supplier Concentration](figures/02_fy26_concentration_map.png)

Supplier concentration was evaluated using the distribution of award values and HHI.

The results help identify categories where procurement awards are concentrated among relatively few suppliers.

These findings should be treated as indicators for further investigation rather than direct evidence of supply chain risk.

### 3. Supplier Exposure

![Supplier Exposure](figures/03_supplier_exposure.png)

This analysis examines how much disclosed award value is associated with individual suppliers.

High exposure to a supplier may be relevant when evaluating sourcing alternatives. However, the dataset does not provide information about supplier capacity, contractual restrictions, or operational reliability.

### 4. Diversification Scenario Analysis

![Diversification Scenario](figures/04_scenario_sensitivity.png)

A hypothetical diversification scenario was used to examine how supplier concentration might change if part of the largest supplier's award value were redistributed.

The scenario illustrates the mathematical effect of diversification on concentration.

It does not establish that redistribution would be operationally feasible or lead to cost savings.

### 5. Data Quality Assessment

![Data Quality](figures/05_missingness.png)

Before interpreting the results, the dataset was examined for missing values and potential limitations.

Missing contract values are particularly important because concentration measures based only on disclosed values may not represent the complete procurement portfolio.

## Discussion

One of the main findings is that procurement concentration needs to be interpreted in context.

A category with a high concentration score may require further evaluation, but it would be misleading to conclude that its sourcing strategy is inefficient based on HHI alone.

Similarly, diversification may reduce measured concentration without necessarily improving procurement outcomes.

This shows why quantitative indicators are useful for identifying questions that purchasing teams should investigate, rather than automatically determining which sourcing decisions should be made.

## Purchasing Recommendations

**1. Prioritize high-value categories for further review.**

Consulting and Contract Consultants account for a large share of disclosed FY2026 award value. Reviewing these categories could help identify where more detailed supplier and contract analysis would be useful.

**2. Investigate concentrated supplier relationships.**

Categories with relatively high supplier concentration should be examined to understand whether the concentration reflects specialization, contractual requirements, or limited sourcing alternatives.

**3. Evaluate diversification before implementation.**

Supplier diversification should be considered alongside costs, supplier capabilities, and operational constraints. A lower concentration score alone is not sufficient evidence that diversification would be beneficial.

## Limitations

This analysis has several limitations.

First, the dataset contains contract award values rather than actual purchasing expenditure or comparable unit prices.

Second, delivery reliability, product quality, and supplier capacity are not available. Therefore, the project cannot directly measure supplier operational performance.

Third, some contract values are missing or estimated, which may affect concentration measures.

Finally, the diversification scenarios are hypothetical. They demonstrate how sourcing allocation could affect concentration, but they do not estimate realized savings.

For these reasons, the results should be interpreted as a starting point for procurement evaluation rather than a complete sourcing recommendation.

## Reusable Analytics Toolkit

In addition to the World Bank case study, this repository contains reusable Python functions for procurement and supply chain analysis.

The toolkit includes modules for:

- Data quality checks
- Procurement analysis
- Supplier concentration
- Supplier delivery metrics
- Inventory analysis
- Sourcing scenario evaluation

These functions can be adapted to other datasets, provided that the necessary variables are available.

## Repository Structure

- `data/raw/` — Original procurement dataset
- `src/` — Reusable Python analysis modules
- `notebooks/` — Jupyter Notebooks
- `figures/` — Visualizations
- `outputs/` — Calculated metrics and analytical tables
- `reports/` — Executive summary
- `tests/` — Automated tests
- `build_portfolio.py` — Portfolio report generation
- `run_analysis.py` — Analysis pipeline
- `requirements.txt` — Python dependencies

## Reproducing the Analysis

Install the required packages:

```bash
pip install -r requirements.txt
```

Generate the portfolio outputs:

```bash
python build_portfolio.py
```

Run the analysis pipeline:

```bash
python run_analysis.py
```

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

## Data Source and Attribution

World Bank Group. *Corporate Procurement Contract Awards* (DS00028).

https://financesone.worldbank.org/d/DS00028

Downloaded November 7, 2026.

License: Creative Commons Attribution 4.0 International.

## Responsible Use

This project was developed with AI assistance. The analysis is based on publicly available procurement records and does not represent internal purchasing data from P&G or another FMCG company.

The results should not be interpreted as evidence of realized cost savings, supplier delivery performance, or the operational feasibility of specific sourcing decisions.
