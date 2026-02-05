"""Interactive tour/walkthrough for Materials Priority Tool."""

import streamlit as st

# Tour steps configuration
TOUR_STEPS = [
    {
        "title": "Welcome to the Materials Priority Tool",
        "content": """
This tool helps you prioritize critical materials for domestic production by scoring
and ranking them across 5 key factors.

**What you'll learn:**
- How materials are scored and ranked
- How to explore individual material profiles
- How to adjust weights for your priorities
- How to export data and save scenarios
        """,
        "page": "Home",
    },
    {
        "title": "Understanding the Scoring Framework",
        "content": """
Each material is scored on **5 factors** (1-10 scale):

| Factor | Weight | Higher Score Means |
|--------|--------|-------------------|
| Supply Risk | 25% | More vulnerable supply chain |
| Market Opportunity | 20% | Better growth/price potential |
| KC Advantage | 15% | Better fit for Kansas City |
| Production Feasibility | 20% | Easier to produce domestically |
| Strategic Alignment | 20% | Higher national priority |

The **composite score** is a weighted average of these factors.
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
- 🏷️ **Score breakdown** — All 5 factor scores explained
- 🌍 **Supply chain overview** — Import reliance, top producers
- 💰 **Market data** — Prices, growth projections
- 🏭 **KC advantage details** — Why KC is (or isn't) a good fit
- 📋 **DOE assessment** — Official criticality ratings

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
- "Supply Security Focus" — Prioritizes reducing import dependence
- "Market Opportunity Focus" — Prioritizes growth potential
- "KC Advantage Focus" — Prioritizes local logistics fit
        """,
        "page": "Trade-off Analysis",
    },
    {
        "title": "Market Monitor Page",
        "content": """
**Navigate to: Market Monitor** (sidebar)

Track market dynamics:
- 💵 **Current prices** — 2024 prices and 5-year changes
- 📈 **Demand growth** — Projected annual growth rates
- 🔴 **Import reliance** — Visual risk indicators
- 🔥 **Correlation heatmap** — How metrics relate to each other

**Key insight:** Materials with high import reliance AND high demand growth
are the most strategically important to prioritize.
        """,
        "page": "Market Monitor",
    },
    {
        "title": "Uncertainty Analysis Page",
        "content": """
**Navigate to: Uncertainty Analysis** (sidebar)

This is the most advanced feature — Monte Carlo simulation:
- 🎲 **Run 1000+ simulations** with randomized inputs
- 📊 **See ranking probabilities** — "Lithium is #1 in 73% of scenarios"
- 📈 **Score distributions** — Box plots showing uncertainty ranges
- 🎯 **Confidence levels** — Know how certain your rankings are

**Why it matters:**
Real data has uncertainty. This tells you whether Lithium is
*definitely* #1, or if Graphite has a 40% chance of taking the top spot.
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
- **Trade-offs** → Test different strategies
- **Market Monitor** → Track market conditions
- **Uncertainty** → Understand ranking confidence

**Next steps:**
1. Check the Priority Rankings to see current recommendations
2. Adjust weights in Trade-off Analysis to match your priorities
3. Run Monte Carlo simulation to understand confidence levels
4. Export a PDF report to share with stakeholders

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
