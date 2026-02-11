# Materials Priority Tool

A data-driven decision support dashboard for scoring and ranking critical materials for domestic production prioritization.

**🔗 [Live Demo](https://materials-priority-tool.streamlit.app)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://materials-priority-tool.streamlit.app)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Why This Tool?

Critical materials decisions are often made using outdated reports, gut instinct, or opaque methodologies. This tool provides:

- **100% Traceable Data** — Every number links to USGS or DOE source documents
- **Interactive What-If Analysis** — Adjust weights, see rankings change instantly
- **Uncertainty Quantification** — Know your confidence level, not just the ranking
- **Open Methodology** — No black box; verify any calculation yourself

---

## Materials Covered

Evaluates **13 critical materials** essential to battery, clean energy, defense, and semiconductor supply chains:

| Material | DOE Category | Primary Use |
|----------|--------------|-------------|
| Rare Earths | Critical | Magnets |
| Gallium | Critical | Semiconductor |
| Graphite | Critical | Battery |
| Cobalt | Critical | Battery |
| Platinum Group | Near-Critical | Fuel Cell |
| Lithium | Near-Critical | Battery |
| Nickel | Near-Critical | Battery |
| Copper | Near-Critical | EV/Grid |
| Manganese | Not-Evaluated | Battery |
| Vanadium | Not-Evaluated | Grid Storage |
| Tin | Not-Evaluated | Electronics |
| Tungsten | Not-Evaluated | Defense |
| Zinc | Not-Evaluated | Galvanizing |

---

## Scoring Framework

Materials are scored using a **3-factor model** based entirely on verified government data:

| Factor | Weight | What It Measures | Data Source |
|--------|--------|------------------|-------------|
| **Supply Risk** | 40% | Import reliance + producer concentration | USGS MCS 2024 |
| **Strategic Alignment** | 40% | DOE criticality category | DOE 2023 Assessment |
| **Production Feasibility** | 20% | Whether US production exists | USGS MCS 2024 |

The **composite score** is the weighted sum. Weights are adjustable in the Trade-off Analysis page.

> *This framework is extensible. Additional factors can be incorporated as verified data becomes available.*

---

## Dashboard Pages

| Page | Purpose |
|------|---------|
| **Home** | Executive summary, top priorities, quick actions |
| **Priority Rankings** | Full rankings table with CSV/Excel/PDF export |
| **Material Deep Dives** | Individual material profiles with supply chain details |
| **Trade-off Analysis** | Adjust weights, save scenarios, compare strategies |
| **Supply Chain Monitor** | Import reliance, producer concentration, DOE categories |
| **Uncertainty Analysis** | Monte Carlo simulation for ranking confidence |

---

## Data Provenance

All data is verified and traceable:

| Source | Description |
|--------|-------------|
| [USGS Mineral Commodity Summaries 2024](https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries) | Import reliance, top producers, US production status |
| [DOE Critical Materials Assessment 2023](https://www.energy.gov/eere/vehicles/articles/2023-critical-materials-assessment) | Criticality categories (Critical, Near-Critical, Not-Critical) |

See [`DATA_SOURCES.md`](DATA_SOURCES.md) for complete data provenance documentation.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/deepakdeo/materials-priority-tool.git
cd materials-priority-tool

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
```

The dashboard opens at `http://localhost:8501`

---

## Project Structure

```
materials-priority-tool/
├── Home.py                     # Main Streamlit entry point
├── pages/                      # Dashboard pages
│   ├── 1_Priority_Rankings.py
│   ├── 2_Material_Deep_Dives.py
│   ├── 3_Tradeoff_Analysis.py
│   ├── 4_Market_Monitor.py
│   └── 5_Uncertainty_Analysis.py
├── src/                        # Core modules
│   ├── data_processor.py       # Scoring calculations
│   ├── data_loader.py          # Data loading functions
│   └── utils.py                # Export utilities
├── data/
│   ├── reference/              # Verified source data (CSV)
│   └── processed/              # Generated outputs
├── DATA_SOURCES.md             # Complete data provenance
└── requirements.txt
```

---

## Use Cases

- **Investment prioritization** — Which materials deserve focus?
- **Supply chain risk assessment** — Where are the vulnerabilities?
- **Scenario planning** — How do rankings change under different priorities?
- **Stakeholder communication** — Exportable reports with traceable data

---

## Author

**Deepak Deo**
[GitHub](https://github.com/deepakdeo) • [LinkedIn](https://linkedin.com/in/deepakdeo)

---

## License

MIT

---

Built with [Streamlit](https://streamlit.io) | Data from [USGS](https://www.usgs.gov) & [DOE](https://www.energy.gov)
