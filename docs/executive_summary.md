# Materials Priority Tool
## Executive Summary

### Purpose

This decision-support dashboard helps organizations prioritize critical materials for domestic production by scoring and ranking six key battery and clean energy materials: **Lithium, Cobalt, Nickel, Graphite, Rare Earths, and Manganese**.

The tool answers a critical question: **"Which materials should we prioritize for domestic production, and why?"**

---

### Scoring Framework

Materials are evaluated across five weighted factors:

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Supply Risk** | 25% | U.S. import dependency, geographic concentration of global production |
| **Market Opportunity** | 20% | Price trends, demand growth projections, market size |
| **KC Advantage** | 15% | Kansas City logistics benefits (rail hub, river access, central location) |
| **Production Feasibility** | 20% | Domestic production maturity, technology readiness, capital intensity |
| **Strategic Alignment** | 20% | DOE criticality rating, battery/EV/defense relevance |

Each factor is scored 1-10, producing a weighted composite score for ranking.

---

### Key Findings

#### Priority Rankings (Default Weights)

| Rank | Material | Score | Key Insight |
|------|----------|-------|-------------|
| **1** | Lithium | 6.82 | Highest market opportunity (180% 5-year price growth, 20% annual demand growth) |
| **2** | Graphite | 6.76 | Critical supply risk (100% import reliant, 77% from China) |
| **3** | Rare Earths | 6.28 | Critical DOE rating, 95% import reliant, 70% China concentration |
| **4** | Manganese | 6.05 | High supply risk with strong KC logistics advantage |
| **5** | Nickel | 6.04 | Best production feasibility (existing U.S. production, mature technology) |
| **6** | Cobalt | 6.01 | High supply risk but declining prices (-15% over 5 years) |

#### Critical Supply Chain Vulnerabilities

- **Graphite & Manganese**: 100% import reliant
- **Rare Earths**: 95% import reliant, dominated by China (70%)
- **Cobalt**: 76% import reliant, 74% from DRC (geopolitical risk)

#### Market Growth Leaders

- **Lithium**: 20% annual demand growth, $8.5B market
- **Graphite**: 15% annual demand growth, driven by battery anode demand
- **Rare Earths**: 12% annual demand growth, critical for EV motors

---

### Kansas City Advantages

KC's logistics infrastructure provides competitive advantages for bulk material processing:

| Advantage | Relevance |
|-----------|-----------|
| **2nd largest rail yard in U.S.** | Bulk material transport cost savings |
| **Missouri River access** | Barge transport for heavy materials |
| **Central U.S. location** | Minimizes max shipping distance to any coast |
| **Highway intersection** | I-70, I-35, I-29, I-49 connectivity |

**Best KC fit**: Manganese, Graphite, Lithium (bulk transport benefits)

---

### Interactive Features

The dashboard provides:

1. **Priority Rankings** — Sortable table with visualizations (bar chart, radar chart, criticality matrix)
2. **Material Deep Dives** — Individual profiles with supply chain details and score breakdowns
3. **Trade-off Analysis** — Adjustable weight sliders to explore different prioritization scenarios
4. **Market Monitor** — Price trends, demand growth, and supply concentration metrics

---

### Data Sources

| Source | Description | Link |
|--------|-------------|------|
| **USGS Mineral Commodity Summaries 2024** | Production, imports, exports, prices | [usgs.gov/mcs](https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries) |
| **DOE 2023 Critical Materials Assessment** | Criticality ratings (Importance to Energy, Supply Risk) | [energy.gov/critical-materials](https://www.energy.gov/eere/vehicles/articles/2023-critical-materials-assessment) |
| **World Bank Pink Sheet** | Historical commodity prices | [worldbank.org/commodities](https://www.worldbank.org/en/research/commodity-markets) |
| **Bureau of Transportation Statistics** | KC logistics metrics | [bts.gov](https://www.bts.gov/) |

---

### Recommendations

Based on the analysis:

1. **Immediate focus**: Lithium and Graphite — highest combined scores for market opportunity and supply risk
2. **Strategic investment**: Rare Earths — critical for clean energy, severe supply concentration
3. **KC opportunity**: Manganese processing — excellent logistics fit, 100% import reliant
4. **Monitor**: Cobalt prices — high risk but currently declining market

---

### Technical Notes

- Scores are normalized to 1-10 scale for comparability
- Weights are adjustable via the Trade-off Analysis page
- Data reflects 2024 estimates; real-time prices require LME/industry subscriptions
- Dashboard deployed on Streamlit Cloud for easy access

---

*Materials Priority Tool | Data-driven decision support for critical materials prioritization*
