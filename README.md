# Materials Priority Tool

A Streamlit decision-support dashboard for scoring and ranking critical materials to help organizations decide which materials to prioritize for domestic production.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://materials-priority-tool.streamlit.app)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Demo

### Dashboard Overview
![Dashboard Home](docs/screenshots/dashboard-home.png)
*The main dashboard showing top priority materials, key metrics, and score overview chart.*

### Priority Rankings
![Priority Rankings](docs/screenshots/priority-rankings.png)
*Complete material rankings with composite scores, radar chart comparison, and criticality matrix.*

### Trade-off Analysis
![Trade-off Analysis](docs/screenshots/tradeoff-analysis.png)
*Interactive weight adjustment to explore different prioritization scenarios.*

> **Note:** Screenshots coming soon. Run the app locally or visit the [live demo](https://materials-priority-tool.streamlit.app) to see it in action.

## Overview

This tool evaluates **13 critical materials** essential to battery, clean energy, defense, and semiconductor supply chains:

| Material | DOE Category | Primary Use |
|----------|--------------|-------------|
| Lithium | Near-Critical | Battery |
| Cobalt | Critical | Battery |
| Nickel | Near-Critical | Battery |
| Graphite | Critical | Battery |
| Rare Earths | Critical | Magnet |
| Manganese | Lower-Risk | Battery |
| Copper | Near-Critical | EV/Grid |
| Platinum Group | Critical | Fuel Cell |
| Gallium | Critical | Semiconductor |
| Vanadium | Near-Critical | Grid Storage |
| **Tin** | Lower-Risk | Electronics |
| **Tungsten** | Critical | Defense |
| **Zinc** | Near-Critical | Galvanizing |

## Features

- **5-Factor Scoring Framework** — Supply Risk, Market Opportunity, KC Advantage, Production Feasibility, Strategic Alignment
- **Interactive Weight Adjustment** — Customize weights and save scenarios
- **Material Deep Dives** — Detailed profiles with supply chain data and DOE assessments
- **Market Monitor** — Price trends, demand growth, and import reliance visualization
- **Monte Carlo Simulation** — Uncertainty analysis for ranking confidence
- **Export Options** — Download data as CSV, Excel, or PDF reports
- **Dark Mode** — Toggle between light and dark themes
- **Mobile Responsive** — Works on tablets and mobile devices
- **Feedback Widget** — Built-in user feedback collection

## Scoring Framework

Materials are scored on five factors (1-10 scale), with adjustable weights:

| Factor | Default Weight | Measures |
|--------|---------------|----------|
| Supply Risk | 25% | Import dependency, geographic concentration |
| Market Opportunity | 20% | Price trends, demand growth projections |
| KC Advantage | 15% | Kansas City logistics benefits (rail, river, central location) |
| Production Feasibility | 20% | Domestic production technology readiness |
| Strategic Alignment | 20% | DOE criticality rating, national priorities |

The **composite score** is the weighted sum of individual factor scores.

## Dashboard Pages

1. **Home** — Key metrics, top 5 materials, and quick actions
2. **Priority Rankings** — Complete rankings with export options (CSV, Excel, PDF)
3. **Material Deep Dives** — Individual material profiles with gauges and radar charts
4. **Trade-off Analysis** — Interactive weight adjustment and scenario saving
5. **Market Monitor** — Price trends, supply concentration, and correlation heatmaps
6. **Uncertainty Analysis** — Monte Carlo simulation for ranking confidence intervals

## Installation

```bash
# Clone the repository
git clone https://github.com/deepakdeo/materials-priority-tool.git
cd materials-priority-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Process the data (first time only)
python -m src.data_processor
```

## Usage

### Local Development

```bash
# Run the Streamlit app
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app" and select:
   - Repository: `your-username/materials-priority-tool`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy"

The app will be live at `https://your-app-name.streamlit.app`

## Data Sources

| Source | Description | Link |
|--------|-------------|------|
| **USGS Mineral Commodity Summaries 2024** | Production, imports, prices | [usgs.gov/mcs](https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries) |
| **DOE Critical Materials Assessment 2023** | Criticality ratings | [energy.gov](https://www.energy.gov/eere/vehicles/articles/2023-critical-materials-assessment) |
| **World Bank Pink Sheet** | Historical commodity prices | [worldbank.org](https://www.worldbank.org/en/research/commodity-markets) |
| **Bureau of Transportation Statistics** | KC logistics metrics | [bts.gov](https://www.bts.gov/) |

See the [Data Refresh Guide](docs/data_refresh_guide.md) for update instructions.

## Project Structure

```
materials-priority-tool/
├── app.py                  # Main Streamlit entry point
├── pages/                  # Multi-page dashboard views
│   ├── 1_Priority_Rankings.py
│   ├── 2_Material_Deep_Dives.py
│   ├── 3_Tradeoff_Analysis.py
│   ├── 4_Market_Monitor.py
│   └── 5_Uncertainty_Analysis.py
├── src/                    # Core Python modules
│   ├── data_processor.py   # Data processing pipeline
│   ├── scoring.py          # Scoring engine
│   ├── visualizations.py   # Plotly charts
│   ├── theme.py            # Dark/light mode
│   ├── feedback.py         # Feedback widget
│   └── utils.py            # Utilities and exports
├── data/
│   ├── raw/                # Source data files
│   ├── processed/          # Cleaned data (materials_master.csv)
│   └── reference/          # Static reference data
├── tests/                  # Test suite (pytest)
└── docs/                   # Documentation
```

## Use Case

This tool is designed for:
- Regional innovation engines focused on critical materials
- Supply chain analysts evaluating material priorities
- Policy makers assessing domestic production opportunities
- Organizations building battery/clean energy supply chains
- Defense supply chain planners

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

---

Built with [Streamlit](https://streamlit.io) | Data from [USGS](https://www.usgs.gov) and [DOE](https://www.energy.gov)
