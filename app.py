import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(page_title="FusionMart Analytics Dashboard", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# Premium Color Palette
COLORS = ['#6366f1', '#ec4899', '#10b981', '#f59e0b', '#3b82f6', '#8b5cf6', '#14b8a6', '#f43f5e']

st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #e2e8f0;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    /* Metric Cards Glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(99, 102, 241, 0.5);
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    /* Headers in Metric */
    div[data-testid="stMetricLabel"] > div {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] > div {
        color: #f8fafc;
        font-size: 2.2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to style Plotly charts consistently
def apply_premium_layout(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#cbd5e1"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    try:
        sales = pd.read_csv("data/sales.csv", parse_dates=['order_date'])
        
        # Load customers
        customers = pd.read_csv("data/customers.csv") if os.path.exists("data/customers.csv") else pd.DataFrame()
        
        # Merge if possible
        if not customers.empty and 'customer_id' in sales.columns and 'customer_id' in customers.columns:
            sales = sales.merge(customers, on='customer_id', how='left')
            
        return sales
    except Exception as e:
        return pd.DataFrame()

sales_df = load_data()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3256/3256013.png", width=60)
st.sidebar.title("FusionMart Center")
st.sidebar.markdown("---")

sections = [
    "1. Executive Summary",
    "2. Time-Series Performance",
    "3. Regional Analysis",
    "4. Product & Category",
    "5. Customer Analytics",
    "6. Salesperson & Channels",
    "7. Strategic Action Plan"
]
page = st.sidebar.radio("Navigate Sections", sections)

st.sidebar.markdown("---")
show_static = st.sidebar.checkbox("📸 Show Static Reference Images", value=False)
if show_static:
    st.sidebar.info("Static images from the original Markdown report will be rendered where applicable.")

def render_static_images():
    if not show_static: return
    img_dir = "img analysis"
    if not os.path.exists(img_dir): return
    all_imgs = glob.glob(f"{img_dir}/*.jpg")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("### 📸 Static Reference Images")
    cols = st.columns(3)
    idx = 0
    for img in all_imgs:
        cols[idx % 3].image(img, use_container_width=True)
        idx += 1


st.title("🚀 FusionMart Analytics Dashboard")
st.markdown("<span style='color:#94a3b8;'>*Comprehensive Data Analysis (2021-2024)*</span>", unsafe_allow_html=True)
st.markdown("---")

if sales_df.empty:
    st.error("⚠️ Data not found! Please ensure data/sales.csv exists.")
    st.stop()

# Clean up column names for dynamic usage
rev_col = 'sales_amount' if 'sales_amount' in sales_df.columns else 'revenue'
profit_col = 'profit'
qty_col = 'quantity'

# ==========================================
# SECTION 1: EXECUTIVE SUMMARY
# ==========================================
if page == "1. Executive Summary":
    st.header("Executive Summary")
    st.markdown("> **BLUF:** FusionMart generated significant revenue with strong institutional traction, but faces margin pressures in its core laptop category and regional imbalances.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    total_rev = sales_df[rev_col].sum()
    total_profit = sales_df[profit_col].sum()
    margin = (total_profit / total_rev) * 100 if total_rev > 0 else 0
    total_orders = sales_df['order_id'].nunique() if 'order_id' in sales_df.columns else len(sales_df)
    aov = total_rev / total_orders if total_orders > 0 else 0
    total_customers = sales_df['customer_id'].nunique() if 'customer_id' in sales_df.columns else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"₹ {total_rev:,.0f}")
    c2.metric("Total Profit", f"₹ {total_profit:,.0f}")
    c3.metric("Blended Margin", f"{margin:.2f}%")
    c4.metric("Avg Order Value", f"₹ {aov:,.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Total Orders", f"{total_orders:,}")
    c6.metric("Distinct Customers", f"{total_customers:,}")
    c7.metric("Total Units Sold", f"{sales_df[qty_col].sum():,}")
    c8.metric("Active Salespersons", f"{sales_df['salesperson_id'].nunique() if 'salesperson_id' in sales_df.columns else 0}")
    
    render_static_images()


# ==========================================
# SECTION 2: TIME-SERIES PERFORMANCE
# ==========================================
elif page == "2. Time-Series Performance":
    st.header("Time-Series & Growth Trends")
    st.markdown("The monthly revenue trend shows FusionMart operating in a clear seasonal pattern with a single dominant peak each calendar year (Diwali season).")
    
    # Monthly aggregation (use 'ME' instead of 'M' to avoid ValueError in Pandas > 2.2)
    df_time = sales_df.set_index('order_date').resample('ME').agg({rev_col: 'sum', profit_col: 'sum'}).reset_index()
    
    fig = go.Figure()
    # Revenue Area with Gradient
    fig.add_trace(go.Scatter(
        x=df_time['order_date'], y=df_time[rev_col], 
        name='Revenue', 
        line=dict(color=COLORS[0], width=4),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.2)'
    ))
    # Profit Line
    fig.add_trace(go.Scatter(
        x=df_time['order_date'], y=df_time[profit_col], 
        name='Profit', 
        line=dict(color=COLORS[2], width=3, dash='dot')
    ))
    fig.update_layout(title="Monthly Revenue & Profit Momentum")
    apply_premium_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    render_static_images()


# ==========================================
# SECTION 3: REGIONAL ANALYSIS
# ==========================================
elif page == "3. Regional Analysis":
    st.header("Regional Geographic Breakdown")
    st.markdown("South India is the clear regional leader, accounting for roughly 34.3% of total revenue. Central India lags materially.")
    
    if 'region' in sales_df.columns:
        reg_df = sales_df.groupby('region').agg({rev_col: 'sum', profit_col: 'sum'}).reset_index().sort_values(rev_col, ascending=False)
        reg_df['Margin %'] = (reg_df[profit_col] / reg_df[rev_col]) * 100
        
        c1, c2 = st.columns([2, 1])
        with c1:
            fig = px.bar(
                reg_df, x='region', y=rev_col, color='region', 
                title="Revenue Dominance by Region", 
                color_discrete_sequence=COLORS,
                text_auto='.2s'
            )
            fig.update_traces(textposition='outside', marker_line_width=0, opacity=0.9)
            apply_premium_layout(fig)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.dataframe(reg_df.style.format({rev_col: '₹ {:,.0f}', profit_col: '₹ {:,.0f}', 'Margin %': '{:.2f}%'}))
            
    render_static_images()


# ==========================================
# SECTION 4: PRODUCT & CATEGORY
# ==========================================
elif page == "4. Product & Category":
    st.header("Product & Category Performance")
    st.markdown("Laptops dominate the portfolio (81.7% of total revenue) but carry the lowest category margin (13.87%). Accessories deliver a category-leading 49.69% margin.")
    
    if 'category' in sales_df.columns:
        cat_df = sales_df.groupby('category').agg({rev_col: 'sum', profit_col: 'sum'}).reset_index()
        cat_df['Margin %'] = (cat_df[profit_col] / cat_df[rev_col]) * 100
        
        c1, c2 = st.columns(2)
        with c1:
            # Premium Donut Chart
            fig = go.Figure(data=[go.Pie(
                labels=cat_df['category'], 
                values=cat_df[rev_col], 
                hole=.6, 
                marker_colors=COLORS,
                textinfo='percent+label'
            )])
            fig.update_layout(title="Revenue Composition")
            apply_premium_layout(fig)
            # Remove legend for cleaner look on donut
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            cat_df = cat_df.sort_values('Margin %')
            fig2 = px.bar(
                cat_df, x='Margin %', y='category', orientation='h', 
                title="Profit Margin % by Category",
                color='Margin %', color_continuous_scale=['#f43f5e', '#f59e0b', '#10b981']
            )
            apply_premium_layout(fig2)
            st.plotly_chart(fig2, use_container_width=True)
            
    render_static_images()


# ==========================================
# SECTION 5: CUSTOMER ANALYTICS
# ==========================================
elif page == "5. Customer Analytics":
    st.header("Customer Segments & Institutional Skew")
    st.markdown("The customer base reveals a striking B2B/institutional skew. Government and Corporate segments account for the overwhelming majority of revenue.")
    
    if 'customer_segment' in sales_df.columns:
        seg_df = sales_df.groupby('customer_segment').agg({rev_col: 'sum', profit_col: 'sum'}).reset_index()
        fig = px.treemap(
            seg_df, path=['customer_segment'], values=rev_col, 
            color=rev_col, color_continuous_scale='Purpor',
            title="Revenue Density by Customer Segment"
        )
        fig.update_traces(root_color="rgba(0,0,0,0)", textinfo="label+value+percent parent")
        apply_premium_layout(fig)
        fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Customer Segment data not detected in merged CSV.")
        
    render_static_images()


# ==========================================
# SECTION 6: SALESPERSON & CHANNELS
# ==========================================
elif page == "6. Salesperson & Channels":
    st.header("Sales Channels & Salesperson Performance")
    
    c1, c2 = st.columns(2)
    with c1:
        if 'sales_channel' in sales_df.columns:
            ch_df = sales_df.groupby('sales_channel').agg({rev_col: 'sum'}).reset_index()
            fig = px.pie(
                ch_df, values=rev_col, names='sales_channel', 
                title="Revenue by Channel", hole=0.5,
                color_discrete_sequence=COLORS
            )
            fig.update_traces(textinfo='percent+label')
            apply_premium_layout(fig)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
    with c2:
        if 'salesperson_id' in sales_df.columns:
            sp_df = sales_df.groupby('salesperson_id').agg({rev_col: 'sum'}).reset_index().sort_values(rev_col, ascending=False).head(10)
            fig2 = px.bar(
                sp_df, x='salesperson_id', y=rev_col, 
                title="Top 10 Salespersons", 
                color=rev_col, color_continuous_scale='Teal'
            )
            apply_premium_layout(fig2)
            st.plotly_chart(fig2, use_container_width=True)

    render_static_images()


# ==========================================
# SECTION 7: STRATEGIC ACTION PLAN
# ==========================================
elif page == "7. Strategic Action Plan":
    st.header("Insights & Action Plan")
    st.markdown("Based on the 4-year diagnostic, here are the prioritized recommendations:")
    
    actions = [
        {"Priority": "🔴 High", "Initiative": "Attach-Rate Program", "Impact": "+₹70-100 Cr/yr", "Description": "Bundle Accessories + Smartphones into every FusionBook transaction to lift blended margin."},
        {"Priority": "🔴 High", "Initiative": "East & Central India Expansion", "Impact": "+₹400-600 Cr rev", "Description": "Deploy 8 additional salespeople + localized campaigns."},
        {"Priority": "🟡 Medium", "Initiative": "Campaign Calendar Expansion", "Impact": "+₹300-500 Cr rev", "Description": "Target 14-16 campaigns/year with 2 new festive windows (Eid, Onam/Pongal)."},
        {"Priority": "🟡 Medium", "Initiative": "Key-Account Management", "Impact": "Revenue Protection", "Description": "Dedicated program for top 100 institutional customers to mitigate key-person risk."}
    ]
    
    st.table(pd.DataFrame(actions))
    st.info("The data and findings in this dashboard are strictly confidential to FusionMart Pvt. Ltd.")
