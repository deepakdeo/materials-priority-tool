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

Six critical materials essential to the battery and clean energy supply chain:

- **Lithium** — Core battery material (Near-critical)
- **Cobalt** — Battery cathode (Critical)
- **Nickel** — Battery cathode (Near-critical → Critical)
- **Natural Graphite** — Battery anode (Critical)
- **Rare Earths** — Permanent magnets for EVs/wind (Critical)
- **Manganese** — Battery cathode (Lower-risk)

---

### Navigation

Use the sidebar to navigate between dashboard views:

1. **Priority Rankings** — Composite scores and overall rankings
2. **Material Deep Dives** — Individual material profiles and supply chain details
3. **Trade-off Analysis** — Adjust scoring weights interactively
4. **Market Monitor** — Price trends and volatility analysis

---

### Use Cases

This tool is designed for:
- Regional innovation engines focused on critical materials supply chains
- Supply chain analysts evaluating material priorities
- Policy makers assessing domestic production opportunities
- Organizations building battery and clean energy infrastructure
""")

# Footer
st.markdown("---")
st.caption("Materials Priority Tool | Data sources: USGS, DOE, World Bank")
