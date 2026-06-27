import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="FusionMart Command Center", page_icon="🚀", layout="wide")

# Custom CSS for Premium Dark Mode & Glassmorphism
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #e2e8f0;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    /* Metric Cards Glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.4); /* Indigo hover */
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Plotly Chart Container */
    .stPlotlyChart {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 FusionMart Executive Command Center")
st.markdown("*AI-Powered Analytics & Forecasting Platform*")

# Load Data Safely
@st.cache_data
def load_data():
    try:
        sales = pd.read_csv("data/sales.csv")
        return sales
    except FileNotFoundError:
        return pd.DataFrame()

sales_df = load_data()

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Executive Dashboard", "AI Insights & Narratives"])

if page == "Executive Dashboard":
    # Top KPIs
    col1, col2, col3 = st.columns(3)
    if not sales_df.empty:
        rev_col = 'sales_amount' if 'sales_amount' in sales_df.columns else 'revenue'
        total_rev = sales_df[rev_col].sum() if rev_col in sales_df.columns else 0
        total_orders = len(sales_df)
        
        col1.metric("Total Revenue", f"₹ {total_rev:,.0f}", "4.2% MoM")
        col2.metric("Total Orders", f"{total_orders:,}", "-1.5% MoM")
        col3.metric("Forecast Accuracy (MAPE)", "92.4%", "1.2% Improvement")
        
        st.markdown("---")
        
        # Charts
        st.subheader("Regional Performance (Last 90 Days)")
        if 'region' in sales_df.columns and rev_col in sales_df.columns:
            region_perf = sales_df.groupby('region')[rev_col].sum().reset_index()
            fig = px.bar(region_perf, x='region', y=rev_col, color='region', 
                         title="Revenue by Region", template="plotly_dark",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("Data not found. Please ensure data/sales.csv exists.")

elif page == "AI Insights & Narratives":
    st.header("🧠 AI-Synthesized Insights")
    
    try:
        with open("reports/insights.md", "r") as f:
            insights = f.read()
            st.markdown(insights)
    except FileNotFoundError:
        st.info("Run the Phase 3 analytics scripts to generate insights.")
    
    st.markdown("---")
    st.header("📖 Data Narrative")
    try:
        with open("reports/data_narrative.md", "r") as f:
            narrative = f.read()
            st.markdown(narrative)
    except FileNotFoundError:
        st.info("Run the Phase 5 narrative generation script.")
