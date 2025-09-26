
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Decisioning Agentic Flow Dashboard",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #ff4b4b;
}
.decision-card {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_decisioning_results():
    try:
        with open('decisioning_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Decisioning results not found. Run the agentic flow first.")
        return None

def main():
    st.title("🎯 Decisioning Agentic Flow Dashboard")
    st.markdown("**Intelligent Decision-Making with Autonomous Agents**")

    results = load_decisioning_results()
    if not results:
        return

    # Executive Alert Banner
    st.error("🚨 **CRITICAL ALERT**: Cash flow crisis detected - Immediate action required!")

    # Key Decision Metrics
    st.header("📊 Executive Decision Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Business Health Score",
            "65/100",
            delta="Critical",
            delta_color="inverse"
        )

    with col2:
        st.metric(
            "Outstanding AR",
            "$2.48M",
            delta="98% Overdue",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            "Collection Rate",
            "40%",
            delta="vs 85% Industry",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            "Cash Recovery Target",
            "$1.8M",
            delta="60-120 days",
            delta_color="normal"
        )

    # Strategic Decisions Section
    st.header("⚡ Strategic Decisions Required")

    decisions_data = [
        {
            "Decision": "Emergency Collections Program",
            "Timeline": "48 hours",
            "Impact": "$1M+ recovery",
            "Priority": "Critical",
            "Owner": "CFO"
        },
        {
            "Decision": "Milestone Billing Implementation",
            "Timeline": "30 days",
            "Impact": "40% faster cash",
            "Priority": "High",
            "Owner": "Operations"
        },
        {
            "Decision": "Customer Portfolio Optimization",
            "Timeline": "90 days",
            "Impact": "70% bad debt reduction",
            "Priority": "Medium",
            "Owner": "Sales"
        }
    ]

    decisions_df = pd.DataFrame(decisions_data)
    st.dataframe(decisions_df, use_container_width=True)

    # Financial Analysis
    st.header("💰 Financial Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        # Cash Flow Recovery Projection
        dates = pd.date_range(datetime.now(), periods=180, freq='D')
        current_ar = [2481103] * 180
        recovery_scenario = [max(2481103 - (i * 15000), 500000) for i in range(180)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=current_ar,
            mode='lines',
            name='Current Path',
            line=dict(color='red', dash='dot')
        ))

        fig.add_trace(go.Scatter(
            x=dates,
            y=recovery_scenario,
            mode='lines',
            name='Recovery Scenario',
            line=dict(color='green')
        ))

        fig.update_layout(
            title="AR Recovery Projection",
            xaxis_title="Date",
            yaxis_title="Outstanding AR ($)",
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Business Health Radar
        categories = ['Profitability', 'Cash Flow', 'Operations', 'Customer Risk', 'Growth']
        current_scores = [95, 25, 85, 30, 70]
        target_scores = [95, 85, 90, 80, 85]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=current_scores,
            theta=categories,
            fill='toself',
            name='Current State',
            line_color='red'
        ))

        fig.add_trace(go.Scatterpolar(
            r=target_scores,
            theta=categories,
            fill='toself',
            name='Target State',
            line_color='green',
            opacity=0.6
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Business Health Radar"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Agent Insights
    st.header("🤖 Agent Insights")

    if "agent_results" in results:
        agent_tabs = st.tabs(["Discovery", "Intelligence", "Strategy", "Decision"])

        with agent_tabs[0]:
            st.subheader("🔍 Discovery Agent Findings")
            st.write("**Key Insights:**")
            for insight in results["agent_results"].get("discovery", {}).get("insights", []):
                st.write(f"• {insight}")

        with agent_tabs[1]:
            st.subheader("📊 Intelligence Agent Analysis")
            st.write("**Key Insights:**")
            for insight in results["agent_results"].get("intelligence", {}).get("insights", []):
                st.write(f"• {insight}")

        with agent_tabs[2]:
            st.subheader("🎯 Strategy Agent Recommendations")
            st.write("**Key Insights:**")
            for insight in results["agent_results"].get("strategy", {}).get("insights", []):
                st.write(f"• {insight}")

        with agent_tabs[3]:
            st.subheader("⚡ Decision Agent Synthesis")
            st.write("**Key Insights:**")
            for insight in results["agent_results"].get("decision", {}).get("insights", []):
                st.write(f"• {insight}")

    # Action Items
    st.header("✅ Immediate Action Items")

    action_items = [
        "🚨 Convene emergency leadership meeting (24 hours)",
        "📞 Launch aggressive collections campaign (48 hours)",
        "💻 Fast-track milestone billing implementation (30 days)",
        "👥 Expand collections team with additional resources",
        "📊 Establish weekly executive financial health monitoring"
    ]

    for item in action_items:
        st.write(f"{item}")

    # Sidebar Information
    st.sidebar.header("🎯 Decisioning System")
    st.sidebar.info("""
    **Autonomous Agents Deployed:**
    • Discovery Agent
    • Intelligence Agent
    • Strategy Agent
    • Decision Agent
    • Visualization Agent
    """)

    st.sidebar.header("📊 Data Sources")
    st.sidebar.write("• Oracle FUSION_DEMO")
    st.sidebar.write("• Business Intelligence Models")
    st.sidebar.write("• Strategic Pattern Recognition")

    st.sidebar.header("🔄 Last Analysis")
    st.sidebar.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if st.sidebar.button("🚀 Run New Analysis"):
        st.cache_data.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
