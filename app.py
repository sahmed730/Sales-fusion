import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FusionMart Executive Command Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Color Palette (Black & White Theme) ──────────────
TEAL       = "#ffffff"
DARK_TEAL  = "#e2e8f0"
ORANGE     = "#94a3b8"
GREEN      = "#ffffff"
SAGE       = "#64748b"
RED_SOFT   = "#475569"
NAVY       = "#000000"
INDIGO     = "#000000"

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #000000;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, h4 { color: #ffffff; font-weight: 700; letter-spacing: -0.03em; }

/* KPI card styling */
.kpi-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    min-height: 140px;
    display: flex; flex-direction: column; justify-content: center;
}
.kpi-card:hover { transform: translateY(-6px); box-shadow: 0 20px 40px rgba(255,255,255,0.1); }
.kpi-label { font-size: 0.85rem; font-weight: 500; color: #94a3b8; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-value { font-size: 2rem; font-weight: 800; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(255,255,255,0.03); border-radius: 12px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; color: #94a3b8; font-weight: 600; }
.stTabs [aria-selected="true"] { background: rgba(255,255,255,0.1) !important; color: #ffffff !important; }

/* Sidebar */
section[data-testid="stSidebar"] { background-color: #000000 !important; }

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Table styling */
.dataframe { background: rgba(255,255,255,0.02) !important; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════
CR = 1e7  # 1 Crore = 10 million

@st.cache_data
def load_sales():
    df = pd.read_csv("data/sales.csv", parse_dates=["order_date"])
    return df

@st.cache_data
def load_customers():
    if os.path.exists("data/customers.csv"):
        return pd.read_csv("data/customers.csv")
    return pd.DataFrame()

@st.cache_data
def load_inventory():
    if os.path.exists("data/inventory.csv"):
        return pd.read_csv("data/inventory.csv", parse_dates=["inventory_date"])
    return pd.DataFrame()

@st.cache_data
def load_campaigns():
    if os.path.exists("data/campaigns.csv"):
        return pd.read_csv("data/campaigns.csv", parse_dates=["campaign_start", "campaign_end"])
    return pd.DataFrame()

sales = load_sales()
customers = load_customers()
inventory = load_inventory()
campaigns = load_campaigns()

# Merge customer segment into sales
if not customers.empty and "customer_segment" in customers.columns:
    sales = sales.merge(customers[["customer_id", "customer_name", "customer_segment", "age", "gender"]],
                        on="customer_id", how="left")


# ── Helper: standard Plotly layout ────────────────────────────
def base_layout(fig, title="", height=500):
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="#ffffff", family="Inter"), x=0.5, xanchor="center"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#cbd5e1", size=12),
        margin=dict(l=60, r=40, t=60, b=60),
        height=height,
        legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False, linecolor="rgba(255,255,255,0.1)")
    return fig


# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("<h1 style='text-align:center; font-size:2.4rem; margin-bottom:0;'>FusionMart Executive Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:1rem; margin-top:4px;'>Comprehensive Data Analysis Dashboard &nbsp;•&nbsp; 2021–2024</p>", unsafe_allow_html=True)
st.markdown("---")


# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════
tabs = st.tabs([
    "Executive Summary",
    "Time-Series",
    "Regional",
    "Products",
    "Customers",
    "Channels & Sales",
    "Inventory",
    "Campaigns",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE SUMMARY (img43)
# ═══════════════════════════════════════════════════════════════
with tabs[0]:
    total_rev = sales["sales_amount"].sum()
    total_profit = sales["profit"].sum()
    margin_pct = (total_profit / total_rev * 100) if total_rev else 0
    total_orders = sales["order_id"].nunique()
    aov = total_rev / total_orders if total_orders else 0
    total_customers = sales["customer_id"].nunique()
    total_units = sales["quantity"].sum()
    total_sp = sales["salesperson_id"].nunique()

    # Row 1
    kpi_data_r1 = [
        ("Total Revenue",      f"₹{total_rev/CR:,.2f} Cr",      TEAL),
        ("Total Profit",       f"₹{total_profit/CR:,.2f} Cr",    GREEN),
        ("Avg Profit Margin",  f"{margin_pct:.2f}%",             ORANGE),
        ("Total Orders",       f"{total_orders:,}",               SAGE),
    ]
    kpi_data_r2 = [
        ("Avg Order Value",    f"₹{aov/1e3:,.1f}K",             ORANGE),
        ("Total Customers",    f"{total_customers:,}",            TEAL),
        ("Units Sold",         f"{total_units:,}",                SAGE),
        ("Salespersons",       f"{total_sp}",                     RED_SOFT),
    ]

    cols = st.columns(4)
    for i, (label, value, color) in enumerate(kpi_data_r1):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card" style="border: 2px solid {color};">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color};">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols2 = st.columns(4)
    for i, (label, value, color) in enumerate(kpi_data_r2):
        with cols2[i]:
            st.markdown(f"""
            <div class="kpi-card" style="border: 2px solid {color};">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color};">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<p style='text-align:center; color:#64748b; margin-top:24px; font-size:0.85rem;'>
    Period: 2021-01-01 to 2024-12-31 &nbsp;•&nbsp; Active regions: {sales['region'].nunique()} &nbsp;•&nbsp; Product categories: {sales['category'].nunique()}
    </p>""", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:left; color:#475569; font-size:0.75rem;'>Source: FusionMart internal data (2021–2024)</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 — TIME-SERIES (img47)
# ═══════════════════════════════════════════════════════════════
with tabs[1]:
    monthly = sales.set_index("order_date").resample("ME").agg(
        revenue=("sales_amount", "sum"),
        profit=("profit", "sum"),
    ).reset_index()
    monthly["revenue_cr"] = monthly["revenue"] / CR
    monthly["profit_cr"]  = monthly["profit"]  / CR

    peak_idx = monthly["revenue_cr"].idxmax()
    trough_idx = monthly["revenue_cr"].idxmin()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Revenue area
    fig.add_trace(go.Scatter(
        x=monthly["order_date"], y=monthly["revenue_cr"],
        name="Revenue", mode="lines+markers",
        line=dict(color=TEAL, width=3),
        marker=dict(size=5, color=TEAL),
        fill="tozeroy", fillcolor="rgba(255,255,255,0.15)",
    ), secondary_y=False)

    # Profit dashed line
    fig.add_trace(go.Scatter(
        x=monthly["order_date"], y=monthly["profit_cr"],
        name="Profit", mode="lines+markers",
        line=dict(color=ORANGE, width=2.5, dash="dash"),
        marker=dict(size=4, color=ORANGE),
    ), secondary_y=True)

    # Peak annotation
    fig.add_annotation(
        x=monthly.loc[peak_idx, "order_date"],
        y=monthly.loc[peak_idx, "revenue_cr"],
        text=f"Peak: {monthly.loc[peak_idx, 'order_date'].strftime('%Y-%m-%d')}<br>₹{monthly.loc[peak_idx, 'revenue_cr']:.1f} Cr",
        showarrow=True, arrowhead=2, arrowcolor="#ffffff", arrowwidth=2,
        font=dict(size=11, color="#ffffff", family="Inter"),
        bgcolor="rgba(0,0,0,0.6)", bordercolor="#ffffff",
        ax=0, ay=-50
    )
    # Trough annotation
    fig.add_annotation(
        x=monthly.loc[trough_idx, "order_date"],
        y=monthly.loc[trough_idx, "revenue_cr"],
        text=f"Trough: {monthly.loc[trough_idx, 'order_date'].strftime('%Y-%m-%d')}<br>₹{monthly.loc[trough_idx, 'revenue_cr']:.1f} Cr",
        showarrow=True, arrowhead=2, arrowcolor="#aaaaaa", arrowwidth=2,
        font=dict(size=11, color="#aaaaaa", family="Inter"),
        bgcolor="rgba(0,0,0,0.6)", bordercolor="#aaaaaa",
        ax=40, ay=40
    )

    base_layout(fig, "Monthly Revenue & Profit Trend — MoM Trajectory", height=520)
    fig.update_yaxes(title_text="Monthly Revenue (₹ Cr)", secondary_y=False, tickformat=".0f", ticksuffix=" Cr")
    fig.update_yaxes(title_text="Monthly Profit (₹ Cr)", secondary_y=True, tickformat=".0f", ticksuffix=" Cr")
    fig.update_xaxes(title_text="Month")
    st.plotly_chart(fig, use_container_width=True)

    # Quarterly table
    quarterly = sales.set_index("order_date").resample("QE").agg(
        Revenue=("sales_amount", "sum"), Profit=("profit", "sum"), Orders=("order_id", "nunique")
    ).reset_index()
    quarterly["Revenue"] = quarterly["Revenue"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
    quarterly["Profit"]  = quarterly["Profit"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
    quarterly["Quarter"]  = quarterly["order_date"].dt.to_period("Q").astype(str)
    st.dataframe(quarterly[["Quarter","Revenue","Profit","Orders"]].head(16), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3 — REGIONAL ANALYSIS (img51)
# ═══════════════════════════════════════════════════════════════
with tabs[2]:
    reg = sales.groupby("region").agg(revenue=("sales_amount","sum"), profit=("profit","sum"), orders=("order_id","nunique")).reset_index()
    reg["revenue_cr"] = reg["revenue"] / CR
    reg["profit_cr"]  = reg["profit"]  / CR
    reg["margin"]     = (reg["profit"] / reg["revenue"] * 100).round(2)
    reg = reg.sort_values("revenue_cr", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=reg["region"], y=reg["revenue_cr"], name="Revenue (₹ Cr)",
        marker_color=TEAL, text=reg["revenue_cr"].apply(lambda v: f"{v:,.1f}"),
        textposition="outside", textfont=dict(size=12, color="#f1f5f9"),
    ))
    fig.add_trace(go.Bar(
        x=reg["region"], y=reg["profit_cr"], name="Profit (₹ Cr)",
        marker_color=ORANGE, text=reg["profit_cr"].apply(lambda v: f"{v:,.1f}"),
        textposition="outside", textfont=dict(size=12, color="#f1f5f9"),
    ))
    fig.update_layout(barmode="group")
    base_layout(fig, "Regional Performance — Revenue vs Profit by Region", height=500)
    fig.update_yaxes(title_text="Amount (₹ Crore)")
    st.plotly_chart(fig, use_container_width=True)

    # Top cities and states
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Top 10 Cities by Revenue")
        city_df = sales.groupby("city").agg(Revenue=("sales_amount","sum"), Profit=("profit","sum"), Orders=("order_id","nunique")).reset_index()
        city_df = city_df.sort_values("Revenue", ascending=False).head(10)
        city_df["Revenue"] = city_df["Revenue"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
        city_df["Profit"]  = city_df["Profit"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
        st.dataframe(city_df[["city","Revenue","Profit","Orders"]], use_container_width=True, hide_index=True)
    with c2:
        st.markdown("##### Top 5 States by Profit")
        state_df = sales.groupby("state").agg(Revenue=("sales_amount","sum"), Profit=("profit","sum"), Orders=("order_id","nunique")).reset_index()
        state_df = state_df.sort_values("Profit", ascending=False).head(5)
        state_df["Revenue"] = state_df["Revenue"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
        state_df["Profit"]  = state_df["Profit"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
        st.dataframe(state_df[["state","Revenue","Profit","Orders"]], use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# TAB 4 — PRODUCT & CATEGORY (img58, img59)
# ═══════════════════════════════════════════════════════════════
with tabs[3]:
    # ── Top 10 Products (img58) ───────────────────────────────
    prod = sales.groupby("product_name").agg(revenue=("sales_amount","sum"), profit=("profit","sum"), units=("quantity","sum")).reset_index()
    prod["revenue_cr"] = prod["revenue"] / CR
    prod["profit_cr"]  = prod["profit"]  / CR
    top10 = prod.sort_values("revenue_cr", ascending=True).tail(10)

    fig_prod = go.Figure()
    fig_prod.add_trace(go.Bar(
        y=top10["product_name"], x=top10["revenue_cr"], name="Revenue (₹ Cr)",
        orientation="h", marker_color=TEAL,
        text=top10["revenue_cr"].apply(lambda v: f"{v:,.1f}"), textposition="outside",
        textfont=dict(size=11, color="#f1f5f9"),
    ))
    fig_prod.add_trace(go.Bar(
        y=top10["product_name"], x=top10["profit_cr"], name="Profit (₹ Cr)",
        orientation="h", marker_color=ORANGE,
        text=top10["profit_cr"].apply(lambda v: f"{v:,.1f}"), textposition="outside",
        textfont=dict(size=11, color="#f1f5f9"),
    ))
    fig_prod.update_layout(barmode="group")
    base_layout(fig_prod, "Top 10 Products by Revenue (with Profit Overlay)", height=550)
    fig_prod.update_xaxes(title_text="Amount (₹ Crore)")
    st.plotly_chart(fig_prod, use_container_width=True)

    st.markdown("---")

    # ── Category Margin (img59) ───────────────────────────────
    cat = sales.groupby("category").agg(revenue=("sales_amount","sum"), profit=("profit","sum")).reset_index()
    cat["margin"] = (cat["profit"] / cat["revenue"] * 100).round(2)
    cat = cat.sort_values("margin", ascending=False)

    def margin_color(m):
        if m >= 20: return GREEN
        elif m >= 15: return ORANGE
        else: return RED_SOFT

    bar_colors = [margin_color(m) for m in cat["margin"]]

    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(
        x=cat["category"], y=cat["margin"],
        marker_color=bar_colors,
        text=cat["margin"].apply(lambda v: f"{v:.2f}%"), textposition="outside",
        textfont=dict(size=13, color="#f1f5f9", family="Inter"),
    ))
    # Legend annotations
    fig_cat.add_annotation(x=1.0, y=1.15, xref="paper", yref="paper", text="<b>●</b> ≥20% (Healthy)", font=dict(color=GREEN, size=11), showarrow=False, xanchor="right")
    fig_cat.add_annotation(x=1.0, y=1.08, xref="paper", yref="paper", text="<b>●</b> 15–20% (Moderate)", font=dict(color=ORANGE, size=11), showarrow=False, xanchor="right")
    fig_cat.add_annotation(x=1.0, y=1.01, xref="paper", yref="paper", text="<b>●</b> <15% (Pressure)", font=dict(color=RED_SOFT, size=11), showarrow=False, xanchor="right")

    base_layout(fig_cat, "Profit Margin by Product Category", height=480)
    fig_cat.update_yaxes(title_text="Profit Margin (%)", ticksuffix="%")
    fig_cat.update_layout(showlegend=False)
    st.plotly_chart(fig_cat, use_container_width=True)

    # Category table
    cat_tbl = cat.copy()
    cat_tbl["Revenue"] = cat_tbl["revenue"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
    cat_tbl["Profit"]  = cat_tbl["profit"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
    cat_tbl["Margin %"] = cat_tbl["margin"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(cat_tbl[["category","Revenue","Profit","Margin %"]], use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# TAB 5 — CUSTOMER ANALYTICS (img66, img70)
# ═══════════════════════════════════════════════════════════════
with tabs[4]:
    if "customer_segment" in sales.columns:
        seg = sales.groupby("customer_segment").agg(
            customers=("customer_id","nunique"), revenue=("sales_amount","sum"),
            profit=("profit","sum"), orders=("order_id","nunique")
        ).reset_index()
        seg["revenue_cr"] = seg["revenue"] / CR

        # ── Row 1: Donut + Bar (img66) ───────────────────────
        c1, c2 = st.columns(2)
        with c1:
            fig_donut = go.Figure(data=[go.Pie(
                labels=seg["customer_segment"], values=seg["customers"],
                hole=0.55, marker_colors=[TEAL, ORANGE, SAGE, "#9e9e9e"],
                textinfo="percent+label", textfont=dict(size=12),
                insidetextorientation="horizontal",
            )])
            base_layout(fig_donut, "Customer Count by Segment", height=450)
            fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_donut, use_container_width=True)

        with c2:
            seg_sorted = seg.sort_values("revenue_cr", ascending=False)
            fig_seg_bar = go.Figure()
            fig_seg_bar.add_trace(go.Bar(
                x=seg_sorted["customer_segment"], y=seg_sorted["revenue_cr"],
                marker_color=[TEAL, ORANGE, SAGE, "#9e9e9e"],
                text=seg_sorted["revenue_cr"].apply(lambda v: f"₹{v:,.1f} Cr"),
                textposition="outside", textfont=dict(size=12, color="#f1f5f9"),
            ))
            base_layout(fig_seg_bar, "Revenue Contribution by Segment", height=450)
            fig_seg_bar.update_yaxes(title_text="Revenue (₹ Crore)")
            fig_seg_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_seg_bar, use_container_width=True)

        st.markdown("---")

        # ── Row 2: RFM Bubble Scatter (img70) ────────────────
        st.markdown("##### RFM Customer Map — Frequency vs Recency (size = Monetary spend)")
        max_date = sales["order_date"].max()
        rfm = sales.groupby("customer_id").agg(
            Recency=("order_date", lambda x: (max_date - x.max()).days),
            Frequency=("order_id", "nunique"),
            Monetary=("sales_amount", "sum"),
        ).reset_index()

        # Tercile scoring
        rfm["R_score"] = pd.qcut(rfm["Recency"], 3, labels=[3,2,1]).astype(int)
        rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 3, labels=[1,2,3]).astype(int)
        rfm["M_score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 3, labels=[1,2,3]).astype(int)
        rfm["RFM_total"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

        def rfm_tier(score):
            if score >= 7: return "High value"
            elif score >= 5: return "Mid value"
            else: return "Low value"
        rfm["Tier"] = rfm["RFM_total"].apply(rfm_tier)

        tier_colors = {"High value": GREEN, "Mid value": ORANGE, "Low value": RED_SOFT}
        tier_counts = rfm["Tier"].value_counts()

        fig_rfm = go.Figure()
        for tier in ["High value", "Mid value", "Low value"]:
            subset = rfm[rfm["Tier"] == tier]
            n = tier_counts.get(tier, 0)
            fig_rfm.add_trace(go.Scatter(
                x=subset["Recency"], y=subset["Frequency"],
                mode="markers", name=f"{tier} (n={n:,})",
                marker=dict(
                    size=np.clip(subset["Monetary"] / subset["Monetary"].quantile(0.95) * 20, 4, 40),
                    color=tier_colors[tier], opacity=0.6,
                    line=dict(width=0.5, color="rgba(255,255,255,0.2)"),
                ),
                hovertemplate="Recency: %{x} days<br>Frequency: %{y} orders<br>Spend: ₹%{customdata:,.0f}<extra></extra>",
                customdata=subset["Monetary"],
            ))

        base_layout(fig_rfm, "RFM Customer Map — Frequency vs Recency (size = Monetary spend)", height=550)
        fig_rfm.update_xaxes(title_text="Recency (days since last order) → Lower is better")
        fig_rfm.update_yaxes(title_text="Frequency (distinct orders) → Higher is better")
        st.plotly_chart(fig_rfm, use_container_width=True)

        # Top 10 customers
        st.markdown("##### Top 10 Customers by Total Spend")
        if "customer_name" in sales.columns:
            top_cust = sales.groupby(["customer_id","customer_name"]).agg(
                Spend=("sales_amount","sum"), Orders=("order_id","nunique")
            ).reset_index().sort_values("Spend", ascending=False).head(10)
            top_cust["AOV"] = (top_cust["Spend"] / top_cust["Orders"])
            top_cust["Spend"] = top_cust["Spend"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
            top_cust["AOV"]   = top_cust["AOV"].apply(lambda x: f"₹{x/1e5:,.0f} L")
            st.dataframe(top_cust[["customer_id","customer_name","Spend","Orders","AOV"]], use_container_width=True, hide_index=True)

    else:
        st.warning("Customer segment data not available. Ensure customers.csv is present.")


# ═══════════════════════════════════════════════════════════════
# TAB 6 — CHANNELS & SALESPERSONS (img77, img81)
# ═══════════════════════════════════════════════════════════════
with tabs[5]:
    c1, c2 = st.columns(2)

    # ── Channel Revenue Bar (img77 left) ──────────────────────
    with c1:
        ch = sales.groupby("sales_channel").agg(revenue=("sales_amount","sum")).reset_index()
        ch["revenue_cr"] = ch["revenue"] / CR
        ch = ch.sort_values("revenue_cr", ascending=True)

        fig_ch = go.Figure()
        fig_ch.add_trace(go.Bar(
            y=ch["sales_channel"], x=ch["revenue_cr"],
            orientation="h", marker_color=[SAGE, SAGE, ORANGE, TEAL],
            text=ch["revenue_cr"].apply(lambda v: f"₹{v:,.1f} Cr"),
            textposition="outside", textfont=dict(size=12, color="#f1f5f9"),
        ))
        base_layout(fig_ch, "Revenue by Sales Channel", height=400)
        fig_ch.update_xaxes(title_text="Revenue (₹ Crore)")
        fig_ch.update_layout(showlegend=False)
        st.plotly_chart(fig_ch, use_container_width=True)

    # ── Payment Method Donut (img77 right) ────────────────────
    with c2:
        pay = sales.groupby("payment_method").agg(revenue=("sales_amount","sum")).reset_index()
        pay["revenue_cr"] = pay["revenue"] / CR

        fig_pay = go.Figure(data=[go.Pie(
            labels=pay["payment_method"], values=pay["revenue"],
            hole=0.55, marker_colors=[TEAL, ORANGE, SAGE, "#607d8b", "#9e9e9e"],
            textinfo="percent+label", textfont=dict(size=11),
        )])
        base_layout(fig_pay, "Revenue Share by Payment Method", height=400)
        fig_pay.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_pay, use_container_width=True)

    st.markdown("---")

    # ── Salesperson Leaderboard (img81) ───────────────────────
    sp = sales.groupby("salesperson_id").agg(revenue=("sales_amount","sum"), profit=("profit","sum"), orders=("order_id","nunique")).reset_index()
    sp["revenue_cr"] = sp["revenue"] / CR
    sp["profit_cr"]  = sp["profit"]  / CR
    org_avg = sp["revenue_cr"].mean()
    top_sp = sp.sort_values("revenue_cr", ascending=True).tail(11)

    fig_sp = go.Figure()
    fig_sp.add_trace(go.Bar(
        y=top_sp["salesperson_id"], x=top_sp["revenue_cr"], name="Revenue (₹ Cr)",
        orientation="h", marker_color=TEAL,
        text=top_sp["revenue_cr"].apply(lambda v: f"{v:,.1f}"), textposition="outside",
        textfont=dict(size=11, color="#f1f5f9"),
    ))
    fig_sp.add_trace(go.Bar(
        y=top_sp["salesperson_id"], x=top_sp["profit_cr"], name="Profit (₹ Cr)",
        orientation="h", marker_color=ORANGE,
        text=top_sp["profit_cr"].apply(lambda v: f"{v:,.1f}"), textposition="outside",
        textfont=dict(size=11, color="#f1f5f9"),
    ))
    # Org average reference line
    fig_sp.add_vline(x=org_avg, line_dash="dash", line_color="#aaaaaa", line_width=2,
                     annotation_text=f"Org avg: ₹{org_avg:,.1f} Cr",
                     annotation_font_color="#aaaaaa", annotation_font_size=11)

    fig_sp.update_layout(barmode="group")
    base_layout(fig_sp, "Top 10 Salesperson Leaderboard — Revenue & Profit", height=550)
    fig_sp.update_xaxes(title_text="Amount (₹ Crore)")
    st.plotly_chart(fig_sp, use_container_width=True)

    # Discount table
    st.markdown("##### Discount Analysis by Category")
    disc = sales.groupby("category").agg(
        avg_discount=("discount_percent","mean"),
        total_discount_value=("sales_amount", lambda x: (x * sales.loc[x.index, "discount_percent"] / 100).sum())
    ).reset_index()
    disc["avg_discount"] = disc["avg_discount"].apply(lambda x: f"{x:.2f}%")
    disc["total_discount_value"] = disc["total_discount_value"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
    st.dataframe(disc.rename(columns={"category":"Category","avg_discount":"Avg Discount %","total_discount_value":"Total Discount Value"}),
                 use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# TAB 7 — INVENTORY HEALTH (img88)
# ═══════════════════════════════════════════════════════════════
with tabs[6]:
    if not inventory.empty:
        wh = inventory.groupby("warehouse").agg(
            opening=("opening_stock","sum"), closing=("closing_stock","sum"), restock=("restock_quantity","sum")
        ).reset_index()
        wh["opening_m"] = wh["opening"] / 1e6
        wh["closing_m"] = wh["closing"] / 1e6
        wh["restock_m"] = wh["restock"] / 1e6

        fig_inv = go.Figure()
        fig_inv.add_trace(go.Bar(
            x=wh["warehouse"], y=wh["opening_m"], name="Opening Stock (M units)",
            marker_color=SAGE,
            text=wh["opening_m"].apply(lambda v: f"{v:.1f}"), textposition="outside",
            textfont=dict(size=12, color="#f1f5f9"),
        ))
        fig_inv.add_trace(go.Bar(
            x=wh["warehouse"], y=wh["closing_m"], name="Closing Stock (M units)",
            marker_color=TEAL,
            text=wh["closing_m"].apply(lambda v: f"{v:.1f}"), textposition="outside",
            textfont=dict(size=12, color="#f1f5f9"),
        ))
        fig_inv.add_trace(go.Bar(
            x=wh["warehouse"], y=wh["restock_m"], name="Restock Quantity (M units)",
            marker_color=ORANGE,
            text=wh["restock_m"].apply(lambda v: f"{v:.1f}"), textposition="outside",
            textfont=dict(size=12, color="#f1f5f9"),
        ))
        fig_inv.update_layout(barmode="group")
        base_layout(fig_inv, "Inventory Health by Warehouse — Opening / Closing / Restock", height=520)
        fig_inv.update_yaxes(title_text="Stock (Million Units)")
        st.plotly_chart(fig_inv, use_container_width=True)

        # Low-stock alerts
        latest_date = inventory["inventory_date"].max()
        latest_inv = inventory[inventory["inventory_date"] == latest_date]
        low_stock = latest_inv[latest_inv["closing_stock"] < 500]
        p90 = latest_inv["closing_stock"].quantile(0.90)
        overstock = latest_inv[latest_inv["closing_stock"] > p90]
        turnover_proxy = wh["restock"].sum() / wh["closing"].sum() if wh["closing"].sum() > 0 else 0

        st.markdown(f"""<p style='text-align:center; color:#94a3b8; font-size:0.9rem; margin-top:8px;'>
        Low-stock alerts: {len(low_stock)} SKUs (&lt;500 units, latest snapshot) &nbsp;•&nbsp;
        Overstock alerts: {len(overstock)} SKUs (&gt;p90) &nbsp;•&nbsp;
        Turnover proxy: {turnover_proxy:.2f}×
        </p>""", unsafe_allow_html=True)

    else:
        st.warning("Inventory data not found.")


# ═══════════════════════════════════════════════════════════════
# TAB 8 — CAMPAIGN EFFECTIVENESS (img95)
# ═══════════════════════════════════════════════════════════════
with tabs[7]:
    if not campaigns.empty:
        results = []
        for _, camp in campaigns.iterrows():
            name = camp["campaign_name"]
            start = camp["campaign_start"]
            end = camp["campaign_end"]
            duration = (end - start).days
            if duration <= 0:
                duration = 1

            # Campaign window revenue
            camp_sales = sales[(sales["order_date"] >= start) & (sales["order_date"] <= end)]
            camp_rev = camp_sales["sales_amount"].sum()

            # Baseline (same length period before campaign)
            baseline_start = start - pd.Timedelta(days=duration)
            baseline_end = start - pd.Timedelta(days=1)
            baseline_sales = sales[(sales["order_date"] >= baseline_start) & (sales["order_date"] <= baseline_end)]
            baseline_rev = baseline_sales["sales_amount"].sum()

            lift = ((camp_rev - baseline_rev) / baseline_rev * 100) if baseline_rev > 0 else 0

            results.append({
                "Campaign": name,
                "Campaign Rev": camp_rev,
                "Baseline Rev": baseline_rev,
                "Lift %": round(lift, 1),
            })

        camp_df = pd.DataFrame(results).sort_values("Lift %", ascending=True)

        def lift_color(l):
            if l >= 100: return GREEN
            elif l >= 50: return ORANGE
            else: return RED_SOFT

        bar_colors = [lift_color(l) for l in camp_df["Lift %"]]

        fig_camp = go.Figure()
        fig_camp.add_trace(go.Bar(
            y=camp_df["Campaign"], x=camp_df["Lift %"],
            orientation="h", marker_color=bar_colors,
            text=camp_df["Lift %"].apply(lambda v: f"+{v:.1f}%"), textposition="outside",
            textfont=dict(size=12, color="#f1f5f9", family="Inter"),
        ))

        # 100% threshold line
        fig_camp.add_vline(x=100, line_dash="dash", line_color="#aaaaaa", line_width=2,
                           annotation_text="100% lift threshold",
                           annotation_font_color="#aaaaaa", annotation_font_size=10,
                           annotation_position="top")

        # Legend annotations
        fig_camp.add_annotation(x=1.0, y=1.12, xref="paper", yref="paper", text="<b>●</b> ≥100% lift (Strong)", font=dict(color=GREEN, size=11), showarrow=False, xanchor="right")
        fig_camp.add_annotation(x=1.0, y=1.06, xref="paper", yref="paper", text="<b>●</b> 50–100% lift (Moderate)", font=dict(color=ORANGE, size=11), showarrow=False, xanchor="right")
        fig_camp.add_annotation(x=1.0, y=1.00, xref="paper", yref="paper", text="<b>●</b> <50% lift (Soft)", font=dict(color=RED_SOFT, size=11), showarrow=False, xanchor="right")

        base_layout(fig_camp, "Marketing Campaign Effectiveness — Revenue Lift %", height=560)
        fig_camp.update_xaxes(title_text="Revenue Lift % (campaign vs matched pre-window baseline)", ticksuffix="%")
        fig_camp.update_layout(showlegend=False)
        st.plotly_chart(fig_camp, use_container_width=True)

        # Campaign table
        camp_tbl = camp_df.sort_values("Lift %", ascending=False).copy()
        camp_tbl["Campaign Rev"] = camp_tbl["Campaign Rev"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
        camp_tbl["Baseline Rev"] = camp_tbl["Baseline Rev"].apply(lambda x: f"₹{x/CR:,.0f} Cr")
        camp_tbl["Lift %"] = camp_tbl["Lift %"].apply(lambda x: f"+{x:.1f}%")
        st.dataframe(camp_tbl, use_container_width=True, hide_index=True)

    else:
        st.warning("Campaign data not found.")


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("<p style='text-align:center; color:#475569; font-size:0.75rem;'>Source: FusionMart internal data (2021–2024) &nbsp;|&nbsp; Confidential — Distribution restricted to executive leadership</p>", unsafe_allow_html=True)
