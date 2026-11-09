[README_final_improved.md](https://github.com/user-attachments/files/34593688/README_final_improved.md)

# Strategic Sourcing Intelligence
### Supplier Concent# Supply Chain Analytics Toolkit
### Case Study 01 — Strategic Sourcing Intelligence: World Bank FY2026 Procurement Awards

## Key findings

This project examines how procurement award records can help identify supplier concentration and prioritize sourcing reviews. It uses real World Bank Group contract-award data, rather than simulated supplier performance.

- **713 FY2026 award records**, including **704 with positive disclosed amounts**, totaling **$202.67 million** in disclosed award values. These are contract awards, not actual paid expenditure.
- **77.8% of disclosed FY2026 award value** is in **Contract Consultants ($81.69M)** and **Consulting ($75.97M)**.
- **Audio Visual** has **10 valued awards across seven named suppliers**. Its largest named supplier accounts for **42.4%** of disclosed category value; the top three account for **84.2%**. Its award-value **HHI is 3,043**.
- In a **hypothetical** Audio Visual scenario, reallocating 20% of the largest supplier's award value equally to two new suppliers reduces HHI from **3,043 to 2,431**. This is a concentration calculation, not a savings estimate or a sourcing recommendation by itself.

**Purchasing implication:** Review high-value service categories for contract and supplier segmentation, and investigate Audio Visual's relatively concentrated award allocation before considering sourcing changes.

[Read the executive decision brief](reports/executive_summary.md) · [Explore the analysis notebook](notebooks/02_empirical_fy26_analysis.ipynb) · [Inspect the underlying tables](outputs/)

## Research question

How can published procurement award data be used to identify supplier concentration and support sourcing decisions, and what additional information is needed before those decisions can be implemented?

## Data and approach

The analysis uses the World Bank Group's [Corporate Procurement Contract Awards dataset (DS00028)](https://financesone.worldbank.org/d/DS00028), downloaded on 7 November 2026, under CC BY 4.0. The main sample covers **FY2026 (1 July 2025–30 June 2026)**. The source's reporting threshold changed in Q3 FY2025, so comparisons with earlier years would mix different disclosure rules.

I examine missing award values, award-value concentration across categories and named suppliers, and sensitivity to unusually large awards. Supplier concentration is measured using top-supplier shares and the **Herfindahl–Hirschman Index (HHI)**: the sum of squared percentage shares, on a scale from 0 to 10,000. A larger number means that recorded award value is distributed among fewer suppliers.

For orientation, historical U.S. merger guidance often used **1,500 and 2,500** as market-concentration reference points. Those thresholds are **not** a procurement risk classification here: this project's HHI measures one buyer's *published award allocation*, not suppliers' shares of a relevant market. The 2023 U.S. Merger Guidelines also use a different threshold framework. The useful comparison in this case is primarily between categories and between explicitly stated scenarios.

The source uses separate labels for **Contract Consultants** and **Consulting**. They are treated as distinct categories because the dataset does not establish that their services or contract scopes are comparable. Both are large service-related categories, but their exact operational distinction would require additional category documentation.

## Results and visualizations

### 1. Award value by category

![FY26 disclosed award value by category](figures/01_fy26_category_value.png)

Contract Consultants accounts for **$81.69M (40.3%)** and Consulting for **$75.97M (37.5%)**. Together they account for **77.8%** of the $202.67M disclosed FY2026 total. These two categories are the starting point for a category-level review because of their size, not because the data demonstrates overspending.

### 2. Category concentration

![FY26 supplier concentration map](figures/02_fy26_concentration_map.png)

The **Audio Visual** category has an **HHI of 3,043**, compared with **122** for Contract Consultants and **56** for Consulting. Audio Visual contains only **10 valued awards**, so its concentration result is a useful screening signal rather than a stable measure of long-term dependence. Financial Services has a higher HHI (**5,813**) but only **five valued awards**; the small sample is an important reason not to rank it automatically as the highest operational risk.

### 3. Supplier exposure

![Supplier award-value exposure](figures/03_supplier_exposure.png)

In Audio Visual, the largest named supplier, **AV3 Inc.**, receives **42.4%** of disclosed award value, and the top three named suppliers receive **84.2%**. These are shares of published awards within one category and fiscal year, not shares of the broader supplier market. Supplier-name variants and parent-company relationships have not been fully reconciled.

### 4. Diversification sensitivity

![Hypothetical supplier diversification sensitivity](figures/04_scenario_sensitivity.png)

If **20% of the largest Audio Visual supplier's recorded value** were reassigned equally to **two new suppliers**, the modeled HHI would fall from **3,043 to 2,431**, a reduction of **611 points**. The scenario assumes the value can be redistributed without changing the total and does not model supplier availability, switching costs, service quality, or contract restrictions.

### 5. Data quality

![Missing award-value analysis](figures/05_missingness.png)

Across the full source, **500 of 4,799 records** have missing award amounts. In FY2026, **9 of 713 records (1.3%)** lack a positive disclosed amount. Missing amounts are not treated as zero. The FY2026 supplier and category concentration results therefore describe **disclosed value**, not all procurement commitments.

## What I would recommend to a purchasing team

**1. Start with the two largest service categories.** Contract Consultants and Consulting account for **$157.67M** combined. Before making sourcing changes, separate contracts by service scope, business unit, duration, and comparable requirements. This would help distinguish genuine purchasing opportunities from differences in the services being purchased.

**2. Investigate Audio Visual supplier dependence.** With **42.4%** of disclosed category value going to the largest named supplier and **84.2%** to the top three, request comparable specifications, alternative qualified suppliers, service-level performance, capacity information, and switching costs. The immediate decision is whether a competitive sourcing review is warranted, not whether the largest supplier should be replaced.

**3. Improve supplier identity and reporting quality before setting risk limits.** Reconcile supplier aliases and parent-company relationships, and investigate missing award values. Then recalculate concentration measures on a consistent supplier master. Without this step, apparent diversification may partly reflect inconsistent naming.

## Discussion and limitations

The findings show that high total award value and high supplier concentration are different issues. The two largest service categories have relatively low recorded HHI values, while Audio Visual has a much higher concentration score despite representing a much smaller amount of award value. This is why a purchasing review should consider both **financial exposure** and **supplier dependence** rather than rely on one ranking.

The dataset does not include comparable unit prices, delivered quantities, lead times, service quality, supplier capacity, or realized savings. Some indefinite-delivery contract amounts are estimates. Contract descriptions and durations also vary. Consequently, this study identifies where further purchasing analysis could be useful; it cannot establish that a supplier is unreliable, that a contract is overpriced, or that diversification would reduce costs.

## Reusable toolkit

This repository contains reusable functions in `src/` for data-quality checks, procurement analysis, supplier concentration, inventory metrics, delivery measures, and sourcing scenarios. **Only the relevant procurement and concentration modules are applied in this World Bank case study.** The inventory and delivery functions are intended for future datasets containing the required operational fields.

For example, with another dataset containing `vendor`, `category`, and `amount` columns:

```python
import pandas as pd
from src.data_quality import audit
from src.procurement import category_value
from src.suppliers import concentration

df = pd.read_csv("path/to/purchase_orders.csv")
print(audit(df, required=["vendor", "category", "amount"]))
print(category_value(df, category="category", value="amount"))
print(concentration(df, supplier="vendor", value="amount")["hhi"])
```

This example illustrates column mapping; the functions still require valid input types and appropriate interpretation of the dataset's monetary values.

## Repository structure

- `data/raw/` — source dataset
- `src/` — reusable analytics functions
- `notebooks/` — exploratory and empirical notebooks
- `figures/` — five exported visualizations
- `outputs/` — auditable calculations and sensitivity tables
- `reports/` — executive decision brief
- `examples/` — adaptation example
- `tests/` — automated tests
- `build_portfolio.py` and `run_analysis.py` — analysis pipelines

## Reproduce

From the repository root, with Python installed:

```bash
pip install -r requirements.txt
python build_portfolio.py
python run_analysis.py
python -m unittest discover -s tests -v
```

The main dataset is at `data/raw/world_bank_awards.csv`. For the detailed methodology and limitations, see [the executive decision brief](reports/executive_summary.md).

## Attribution and responsible use

Data: World Bank Group, *Corporate Procurement Contract Awards* (DS00028), CC BY 4.0, downloaded 7 November 2026. This is a study of publicly reported World Bank procurement awards, not an assessment of any company's internal purchasing performance.

The project was developed with AI assistance. Its methods and results should be independently reproduced and understood before being presented as personally completed work. No verified savings, supplier delivery performance, or operationally feasible supplier switch is claimed.
ration and Procurement Risk: A World Bank Case Study

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

License: Creative Commons Attribution 4.0 International.


