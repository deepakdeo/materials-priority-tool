"""Interactive tour/walkthrough for Materials Priority Tool."""

import streamlit as st

# Tour steps configuration
TOUR_STEPS = [
    {
        "title": "Welcome to the Materials Priority Tool",
        "content": """
This tool helps you prioritize critical materials for domestic production using
a **transparent, data-driven methodology**.

**What you'll learn:**
- How materials are scored using verified government data
- How to explore individual material profiles
- How to adjust weights for your priorities
- How to understand ranking confidence
        """,
        "page": "Home",
    },
    {
        "title": "Understanding the Scoring Framework",
        "content": """
Each material is scored on **3 factors** using only verified data:

| Factor | Weight | What It Measures | Source |
|--------|--------|------------------|--------|
| Supply Risk | 40% | Import reliance + producer concentration | USGS MCS 2024 |
| Strategic Alignment | 40% | DOE criticality category | DOE 2023 |
| Production Feasibility | 20% | Whether US production exists | USGS MCS 2024 |

The **composite score** is a weighted average of these factors.

*Every number is traceable to government sources — no black boxes.*
        """,
        "page": "Home",
    },
    {
        "title": "Priority Rankings Page",
        "content": """
**Navigate to: Priority Rankings** (sidebar)

This page shows:
- 📊 **Rankings table** — All materials sorted by composite score
- 📈 **Bar chart** — Visual comparison of scores
- 🎯 **Radar chart** — Top 3 materials factor breakdown
- 📍 **Criticality matrix** — Supply Risk vs Strategic Alignment

**Pro tip:** Use the export buttons to download CSV, Excel, or PDF reports!
        """,
        "page": "Priority Rankings",
    },
    {
        "title": "Material Deep Dives Page",
        "content": """
**Navigate to: Material Deep Dives** (sidebar)

Select any material to see:
- 🏷️ **Score breakdown** — All 3 factor scores with weights
- 🌍 **Supply chain overview** — Import reliance, top producers
- 📋 **DOE assessment** — Official criticality categories (Critical, Near-Critical, Not-Critical)
- 📊 **Radar chart** — Visual score profile

**Pro tip:** Compare materials by opening multiple browser tabs!
        """,
        "page": "Material Deep Dives",
    },
    {
        "title": "Trade-off Analysis Page",
        "content": """
**Navigate to: Trade-off Analysis** (sidebar)

This is where it gets interactive:
- 🎚️ **Adjust weights** — Use sliders to change factor importance
- 📊 **See rankings update** — Watch how priorities shift in real-time
- 💾 **Save scenarios** — Store your custom configurations
- 📥 **Export scenarios** — Download as JSON to share with colleagues

**Example scenarios:**
- "Supply Security Focus" — Weight supply risk at 60%
- "Strategic Focus" — Weight DOE alignment at 60%
- "Feasibility Focus" — Prioritize materials with existing US production
        """,
        "page": "Trade-off Analysis",
    },
    {
        "title": "Supply Chain Monitor Page",
        "content": """
**Navigate to: Supply Chain Monitor** (sidebar)

Track supply chain metrics:
- 🔴 **Import reliance** — Visual risk indicators by material
- 🌍 **Producer concentration** — Who controls supply?
- 📊 **DOE categories** — Distribution of criticality ratings
- 🔥 **Correlation heatmap** — How metrics relate to each other

**Key insight:** Materials with high import reliance AND Critical DOE rating
are the highest priority for domestic production.
        """,
        "page": "Supply Chain Monitor",
    },
    {
        "title": "Uncertainty Analysis Page",
        "content": """
**Navigate to: Uncertainty Analysis** (sidebar)

Monte Carlo simulation shows **how confident** you can be in rankings:
- 🎲 **Run 1000+ simulations** with randomized inputs
- 📊 **See ranking probabilities** — "Rare Earths is #1 in 85% of scenarios"
- 📈 **Score distributions** — Box plots showing uncertainty ranges
- 🎯 **Confidence levels** — High (>80%), Medium (50-80%), Low (<50%)

**Why it matters:**
If two materials swap places in 40% of simulations, that's a close call
worth more research. If one is #1 in 95% of simulations, that's definitive.
        """,
        "page": "Uncertainty Analysis",
    },
    {
        "title": "You're Ready!",
        "content": """
**You've completed the tour!**

Quick reference:
- **Rankings** → See overall priorities
- **Deep Dives** → Explore individual materials
- **Trade-offs** → Test different weight strategies
- **Supply Chain** → Understand import & concentration risks
- **Uncertainty** → Know your confidence level

**Key differentiators of this tool:**
- ✅ 100% traceable data (USGS, DOE sources)
- ✅ Interactive what-if analysis
- ✅ Uncertainty quantification
- ✅ Open methodology — verify any calculation

Happy analyzing! 🔋
        """,
        "page": "Home",
    },
]


def init_tour_state():
    """Initialize tour state in session."""
    if "tour_active" not in st.session_state:
        st.session_state.tour_active = False
    if "tour_step" not in st.session_state:
        st.session_state.tour_step = 0


def start_tour():
    """Start the tour."""
    st.session_state.tour_active = True
    st.session_state.tour_step = 0


def end_tour():
    """End the tour."""
    st.session_state.tour_active = False
    st.session_state.tour_step = 0


def next_step():
    """Go to next tour step."""
    if st.session_state.tour_step < len(TOUR_STEPS) - 1:
        st.session_state.tour_step += 1
    else:
        end_tour()


def prev_step():
    """Go to previous tour step."""
    if st.session_state.tour_step > 0:
        st.session_state.tour_step -= 1


def render_tour_widget():
    """Render the tour widget if tour is active."""
    init_tour_state()

    if not st.session_state.tour_active:
        return

    step = TOUR_STEPS[st.session_state.tour_step]
    total_steps = len(TOUR_STEPS)
    current = st.session_state.tour_step + 1

    # Tour container with styling
    with st.container():
        st.markdown(
            """
            <style>
            .tour-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 10px;
                color: white;
                margin-bottom: 1rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(f"📚 **Tour: {step['title']}** (Step {current}/{total_steps})", expanded=True):
            st.markdown(step["content"])

            if step["page"] != "Home":
                st.info(f"👉 **Go to:** {step['page']} in the sidebar")

            # Navigation buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

            with col1:
                if st.session_state.tour_step > 0:
                    if st.button("← Previous", key="tour_prev"):
                        prev_step()
                        st.rerun()

            with col2:
                if current < total_steps:
                    if st.button("Next →", key="tour_next", type="primary"):
                        next_step()
                        st.rerun()
                else:
                    if st.button("✓ Finish", key="tour_finish", type="primary"):
                        end_tour()
                        st.rerun()

            with col3:
                st.caption(f"Step {current} of {total_steps}")

            with col4:
                if st.button("✕ Exit Tour", key="tour_exit"):
                    end_tour()
                    st.rerun()


def render_tour_button():
    """Render button to start tour."""
    init_tour_state()

    if not st.session_state.tour_active:
        if st.button("🎓 Take a Guided Tour", type="secondary"):
            start_tour()
            st.rerun()
