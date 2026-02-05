# Materials Priority Tool

A Streamlit decision-support dashboard for scoring and ranking critical materials to help organizations decide which materials to prioritize for domestic production.

## Overview

This tool evaluates six critical materials essential to the battery and clean energy supply chain:

| Material | DOE Category | Primary Use |
|----------|--------------|-------------|
| Lithium | Near-Critical | Battery core |
| Cobalt | Critical | Battery cathode |
| Nickel | Near-Critical | Battery cathode |
| Natural Graphite | Critical | Battery anode |
| Rare Earths | Critical | Permanent magnets |
| Manganese | Lower-Risk | Battery cathode |

## Scoring Framework

Materials are scored on five factors (1-10 scale), with adjustable weights:

| Factor | Default Weight | Measures |
|--------|---------------|----------|
| Supply Risk | 25% | Import dependency, geographic concentration |
| Market Opportunity | 20% | Price trends, demand growth |
| KC Advantage | 15% | Kansas City logistics benefits |
| Production Feasibility | 20% | Domestic production readiness |
| Strategic Alignment | 20% | DOE criticality, national priorities |

## Dashboard Pages

1. **Priority Rankings** — Composite scores and overall rankings
2. **Material Deep Dives** — Individual material profiles
3. **Trade-off Analysis** — Interactive weight adjustment
4. **Market Monitor** — Price trends and volatility

## Installation

```bash
# Clone the repository
git clone https://github.com/[username]/materials-priority-tool.git
cd materials-priority-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
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

- **USGS Mineral Commodity Summaries 2025** — Production, imports, prices
- **DOE 2023 Critical Materials Assessment** — Criticality scores
- **World Bank Pink Sheet** — Commodity price trends
- **Bureau of Transportation Statistics** — Regional logistics data

## Project Structure

```
materials-priority-tool/
├── app.py                 # Main Streamlit entry point
├── pages/                 # Multi-page dashboard views
├── src/                   # Core Python modules
│   ├── data_loader.py     # Data loading functions
│   ├── scoring.py         # Scoring engine
│   ├── visualizations.py  # Plotly charts
│   └── utils.py           # Utilities
├── data/
│   ├── raw/               # Source data files
│   ├── processed/         # Cleaned data
│   └── reference/         # Static reference data
└── tests/                 # Test suite
```

## Use Case

This tool is designed for:
- Regional innovation engines focused on critical materials
- Supply chain analysts evaluating material priorities
- Policy makers assessing domestic production opportunities
- Organizations building battery/clean energy supply chains

## License

MIT
