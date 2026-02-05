"""Materials Priority Tool - Main Entry Point.

A Streamlit dashboard for scoring and ranking critical materials
to support supply chain prioritization decisions.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Materials Priority Tool",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main page content
st.title("Materials Priority Tool")

st.markdown("""
A decision-support dashboard for evaluating and prioritizing critical materials
for domestic production.

This tool scores and ranks materials based on five key factors:

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Supply Risk** | 25% | U.S. import dependency, geographic concentration |
| **Market Opportunity** | 20% | Price trends, demand growth projections |
| **KC Advantage** | 15% | Kansas City logistics benefits |
| **Production Feasibility** | 20% | Domestic production technology maturity |
| **Strategic Alignment** | 20% | DOE criticality, battery/EV/defense priorities |

---

### Materials Under Analysis

Ten critical materials essential to the battery, clean energy, and semiconductor supply chains:

| Material | Primary Use | DOE Category |
|----------|-------------|--------------|
| **Lithium** | Battery | Near-Critical |
| **Cobalt** | Battery | Critical |
| **Nickel** | Battery | Near-Critical |
| **Graphite** | Battery | Critical |
| **Rare Earths** | Magnets | Critical |
| **Manganese** | Battery | Lower-Risk |
| **Copper** | EV/Grid | Near-Critical |
| **Platinum Group** | Fuel Cells | Critical |
| **Gallium** | Semiconductors | Critical |
| **Vanadium** | Grid Storage | Near-Critical |

---

### Navigation

Use the sidebar to navigate between dashboard views:

1. **Priority Rankings** — Composite scores, rankings, and data export (CSV/Excel/PDF)
2. **Material Deep Dives** — Individual material profiles and supply chain details
3. **Trade-off Analysis** — Adjust weights interactively, save/load custom scenarios
4. **Market Monitor** — Price trends, correlation heatmap, and supply risk metrics

---

### Key Features

- **Export Data** — Download rankings as CSV, Excel, or PDF report
- **Scenario Analysis** — Save and compare different weight configurations
- **Interactive Visualizations** — Radar charts, stacked bars, correlation heatmaps
- **10 Critical Materials** — Comprehensive coverage of battery, EV, and semiconductor supply chains

---

### Use Cases

This tool is designed for:
- Regional innovation engines focused on critical materials supply chains
- Supply chain analysts evaluating material priorities
- Policy makers assessing domestic production opportunities
- Organizations building battery, clean energy, and semiconductor infrastructure
""")

# Footer
st.markdown("---")
st.caption("Materials Priority Tool | Data sources: USGS, DOE, World Bank")
