# Supplier Concentration and Sourcing Decisions

*An exploratory analysis of World Bank Group procurement awards, FY2026*

## Research question

How can published procurement awards help identify sourcing categories that may need closer review, and what can they tell us about supplier concentration?

## Introduction

One of the main challenges in evaluating purchasing decisions is that cost and supplier reliability cannot always be observed together. A company might work with fewer suppliers to simplify purchasing, but depending too heavily on a small number of suppliers could also create operational risks. This means that supplier concentration is worth examining, although concentration by itself does not tell us whether a purchasing strategy is effective.

This analysis uses publicly available World Bank Group corporate procurement awards. The aim is not to evaluate the Bank's procurement decisions, but to examine how award records can support an initial sourcing review. I focus on FY2026 because the dataset's reporting threshold changed during FY2025, which makes comparisons across longer periods difficult to interpret.

## Data and method

The FY2026 subset contains **713 records**, of which **704 have disclosed positive award values**. Their combined value is approximately **USD 202.67 million**. These figures represent reported contract awards rather than actual payments or unit purchase prices. In the complete dataset, **500 of 4,799 records** have missing award values.

I grouped disclosed values by commodity category and supplier name. To examine concentration, I calculated the largest supplier's share and the Herfindahl-Hirschman Index (HHI), which adds together squared supplier value shares and scales the result to 10,000. A higher score means that the *recorded awards* are more concentrated among fewer named suppliers. It does not measure market concentration or the probability that a supplier will fail.

## Results

The two largest FY2026 categories were **Contract Consultants (USD 81.69 million)** and **Consulting (USD 75.97 million)**. Together, they accounted for **77.8%** of disclosed award value. This suggests that a category review could start with these areas, where even small improvements in purchasing processes may matter. However, the data does not establish that contracts are overpriced or that savings are achievable.

A different pattern appears in **Audio Visual**, which had **10 valued awards**, **seven named suppliers**, and an award-value HHI of approximately **3,043**. This indicates that the recorded award values were relatively concentrated. Still, the number of awards is small, and the data does not show whether the suppliers provided comparable services. Therefore, it would be premature to interpret this result as evidence of a sourcing problem.

I also examined a hypothetical diversification scenario. If 20% of the largest Audio Visual supplier's observed award value were reassigned equally to two new suppliers, the calculated HHI would decrease from about **3,043 to 2,431**. This illustrates how the metric responds to a change in supplier allocation. It does not show that the reassignment is possible, less expensive, or less risky.

## Discussion and purchasing recommendations

**First, prioritize a category-level review of consulting-related awards.** These categories account for most of the published FY2026 value, making them useful places to begin. Before considering negotiation or consolidation, a purchasing team would need to compare contract scopes, durations, and service requirements. Differences in total award values are not necessarily differences in price for the same service.

**Second, improve supplier identification before making concentration decisions.** The analysis uses supplier names as they appear in the source. Different names may refer to the same company, and related companies may appear separately. A verified supplier master would make concentration estimates more meaningful and help distinguish apparent diversity from genuine sourcing alternatives.

**Third, investigate Audio Visual rather than immediately diversifying.** Its concentration score is high enough to justify a closer look, but the dataset does not contain bids, supplier capacity, delivery outcomes, or switching costs. These would be needed before recommending any change to supplier allocation. The scenario analysis is best understood as a way to frame questions for further investigation.

## Limitations

This analysis has several limitations. First, the data contains only published awards meeting disclosure criteria, not all procurement activity. Second, some indefinite-delivery contract amounts are estimates, and missing values were excluded rather than imputed. Third, supplier names have not been fully matched to legal entities. Finally, there is no information on delivery reliability, product quality, comparable unit prices, or realized savings. As a result, the findings can identify areas for review but cannot determine which suppliers should be replaced or whether diversification would improve performance.

## Conclusion

The main finding is not that a particular supplier or category is inefficient. Rather, the analysis shows how procurement records can help organize a sourcing review by separating categories with high reported value from categories with concentrated supplier exposure. I found it especially important that the same metric can be informative while still being insufficient for a final decision. A purchasing recommendation becomes more credible when it explains not only what the available data suggests, but also what additional evidence is needed before acting.

## Source

World Bank Group. *Corporate Procurement Contract Awards* (DS00028), data as of 30 June 2026, downloaded 7 November 2026. CC BY 4.0. https://financesone.worldbank.org/d/DS00028
