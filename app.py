"""
═══════════════════════════════════════════════════════════════════════════════
  GLOBAL INDEX MONTHLY RETURN TRACKER
  The Mountain Path – World of Finance
  Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, date
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Index Return Tracker | The Mountain Path",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  DESIGN CONSTANTS  (Mountain Path palette)
# ─────────────────────────────────────────────
DARK_BLUE   = "#003366"
MID_BLUE    = "#004d80"
CARD_BG     = "#112240"
GOLD        = "#FFD700"
LIGHT_BLUE  = "#ADD8E6"
TEXT_MAIN   = "#e6f1ff"
TEXT_MUTED  = "#8892b0"
GREEN       = "#28a745"
RED         = "#dc3545"
BG_GRAD_1   = "#1a2332"
BG_GRAD_2   = "#243447"
BG_GRAD_3   = "#2a3f5f"

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── ROOT ── */
html, body, [class*="css"] {{
    font-family: 'Source Sans 3', sans-serif;
    background: linear-gradient(135deg, {BG_GRAD_1}, {BG_GRAD_2}, {BG_GRAD_3}) !important;
    color: {TEXT_MAIN};
}}
.stApp {{
    background: linear-gradient(135deg, {BG_GRAD_1}, {BG_GRAD_2}, {BG_GRAD_3}) !important;
}}

/* ── HERO BANNER ── */
.hero-banner {{
    background: linear-gradient(90deg, {DARK_BLUE} 0%, {MID_BLUE} 60%, #1a3a5c 100%);
    border-bottom: 3px solid {GOLD};
    border-radius: 0 0 16px 16px;
    padding: 28px 36px 20px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}}
.hero-banner::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,215,0,0.12) 0%, transparent 70%);
    border-radius: 50%;
}}
.hero-title {{
    font-family: 'Cinzel', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: {GOLD};
    letter-spacing: 1px;
    margin: 0;
    line-height: 1.2;
    -webkit-text-fill-color: {GOLD};
}}
.hero-subtitle {{
    font-size: 0.95rem;
    color: {LIGHT_BLUE};
    margin-top: 6px;
    letter-spacing: 0.5px;
    -webkit-text-fill-color: {LIGHT_BLUE};
}}
.hero-badge {{
    display: inline-block;
    background: rgba(255,215,0,0.15);
    border: 1px solid {GOLD};
    color: {GOLD};
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin-top: 8px;
    letter-spacing: 0.8px;
    font-weight: 600;
    -webkit-text-fill-color: {GOLD};
}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DARK_BLUE} 0%, #001f40 100%) !important;
    border-right: 2px solid {GOLD};
}}
[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}
.sidebar-logo {{
    font-family: 'Cinzel', serif;
    font-size: 1.05rem;
    color: {GOLD};
    font-weight: 700;
    text-align: center;
    padding: 10px 0 4px 0;
    border-bottom: 1px solid rgba(255,215,0,0.3);
    margin-bottom: 16px;
    -webkit-text-fill-color: {GOLD};
}}

/* ── METRIC CARDS ── */
.metric-row {{ display: flex; gap: 14px; margin-bottom: 20px; flex-wrap: wrap; }}
.metric-card {{
    background: linear-gradient(135deg, {CARD_BG} 0%, {DARK_BLUE} 100%);
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 12px;
    padding: 18px 22px;
    flex: 1; min-width: 160px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35);
    transition: transform 0.2s, border-color 0.2s;
    user-select: none;
}}
.metric-card:hover {{ transform: translateY(-3px); border-color: {GOLD}; }}
.metric-label {{
    font-size: 0.72rem;
    color: {TEXT_MUTED};
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
    -webkit-text-fill-color: {TEXT_MUTED};
}}
.metric-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1.1;
}}
.metric-value.positive {{ color: {GREEN}; -webkit-text-fill-color: {GREEN}; }}
.metric-value.negative {{ color: {RED};  -webkit-text-fill-color: {RED}; }}
.metric-value.neutral  {{ color: {GOLD}; -webkit-text-fill-color: {GOLD}; }}
.metric-sub {{
    font-size: 0.75rem;
    color: {TEXT_MUTED};
    margin-top: 4px;
    -webkit-text-fill-color: {TEXT_MUTED};
}}

/* ── SECTION HEADERS ── */
.section-header {{
    font-family: 'Cinzel', serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: {GOLD};
    border-left: 4px solid {GOLD};
    padding-left: 14px;
    margin: 24px 0 14px 0;
    letter-spacing: 0.5px;
    -webkit-text-fill-color: {GOLD};
    user-select: none;
}}

/* ── HEATMAP TABLE ── */
.heatmap-container {{
    background: {CARD_BG};
    border: 1px solid rgba(173,216,230,0.2);
    border-radius: 12px;
    padding: 6px;
    margin-bottom: 22px;
    overflow-x: auto;
}}

/* ── FOOTER ── */
.footer {{
    background: linear-gradient(90deg, {DARK_BLUE}, {MID_BLUE});
    border-top: 2px solid {GOLD};
    border-radius: 12px 12px 0 0;
    padding: 14px 28px;
    margin-top: 36px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    user-select: none;
}}
.footer-name {{
    font-family: 'Cinzel', serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: {GOLD};
    -webkit-text-fill-color: {GOLD};
}}
.footer-links a {{
    color: {GOLD};
    text-decoration: none;
    font-size: 0.8rem;
    margin-left: 18px;
    -webkit-text-fill-color: {GOLD};
}}
.footer-links a:hover {{ text-decoration: underline; }}

/* ── STREAMLIT OVERRIDES ── */
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stDateInput label,
.stRadio label {{ color: {LIGHT_BLUE} !important; font-weight: 600; }}
div[data-testid="stMetric"] {{ background: transparent; }}
.stTabs [data-baseweb="tab-list"] {{ background: {DARK_BLUE}; border-radius: 8px; }}
.stTabs [data-baseweb="tab"] {{ color: {LIGHT_BLUE}; font-weight: 600; }}
.stTabs [aria-selected="true"] {{ color: {GOLD} !important; border-bottom: 3px solid {GOLD}; }}
.stDataFrame {{ border-radius: 10px; }}
.stButton > button {{
    background: linear-gradient(135deg, {DARK_BLUE}, {MID_BLUE});
    color: {GOLD};
    border: 1px solid {GOLD};
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 8px 22px;
    transition: all 0.2s;
}}
.stButton > button:hover {{
    background: {GOLD};
    color: {DARK_BLUE};
    transform: translateY(-1px);
}}
.stCheckbox span {{ color: {TEXT_MAIN} !important; }}
.stInfo, .stWarning, .stSuccess, .stError {{ border-radius: 8px; }}
hr {{ border-color: rgba(255,215,0,0.2); }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INDEX UNIVERSE  (20 Global Indices)
# ─────────────────────────────────────────────
INDICES = {
    # ── Equity
    "S&P 500 (US)":         {"ticker": "^GSPC",  "type": "Equity",    "region": "Americas"},
    "NASDAQ 100 (US)":      {"ticker": "^NDX",   "type": "Equity",    "region": "Americas"},
    "Dow Jones (US)":       {"ticker": "^DJI",   "type": "Equity",    "region": "Americas"},
    "FTSE 100 (UK)":        {"ticker": "^FTSE",  "type": "Equity",    "region": "Europe"},
    "DAX 40 (Germany)":     {"ticker": "^GDAXI", "type": "Equity",    "region": "Europe"},
    "CAC 40 (France)":      {"ticker": "^FCHI",  "type": "Equity",    "region": "Europe"},
    "Nikkei 225 (Japan)":   {"ticker": "^N225",  "type": "Equity",    "region": "Asia-Pacific"},
    "Hang Seng (HK)":       {"ticker": "^HSI",   "type": "Equity",    "region": "Asia-Pacific"},
    "CSI 300 (China)":      {"ticker": "000300.SS","type":"Equity",   "region": "Asia-Pacific"},
    "SENSEX (India)":       {"ticker": "^BSESN", "type": "Equity",    "region": "Asia-Pacific"},
    "NIFTY 50 (India)":     {"ticker": "^NSEI",  "type": "Equity",    "region": "Asia-Pacific"},
    "ASX 200 (Australia)":  {"ticker": "^AXJO",  "type": "Equity",    "region": "Asia-Pacific"},
    "IBOVESPA (Brazil)":    {"ticker": "^BVSP",  "type": "Equity",    "region": "Americas"},
    "MSCI EM":              {"ticker": "EEM",     "type": "Equity",    "region": "Global"},
    # ── Commodity
    "Gold (XAU)":           {"ticker": "GC=F",   "type": "Commodity", "region": "Global"},
    "Silver (XAG)":         {"ticker": "SI=F",   "type": "Commodity", "region": "Global"},
    "WTI Crude Oil":        {"ticker": "CL=F",   "type": "Commodity", "region": "Global"},
    "Brent Crude":          {"ticker": "BZ=F",   "type": "Commodity", "region": "Global"},
    "Natural Gas":          {"ticker": "NG=F",   "type": "Commodity", "region": "Global"},
    "Copper":               {"ticker": "HG=F",   "type": "Commodity", "region": "Global"},
}

TICKER_LIST = {v["ticker"]: k for k, v in INDICES.items()}

# ─────────────────────────────────────────────
#  DATA HELPERS
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_monthly_data(tickers: list, start: str, end: str) -> pd.DataFrame:
    """Fetch adj-close, resample to month-end, compute % returns."""
    raw = yf.download(tickers, start=start, end=end,
                      auto_adjust=True, progress=False)["Close"]
    if isinstance(raw, pd.Series):
        raw = raw.to_frame(name=tickers[0])
    monthly = raw.resample("ME").last()
    returns = monthly.pct_change() * 100
    returns.index = returns.index.to_period("M").astype(str)
    return returns

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_latest_prices(tickers: list) -> dict:
    """Fetch latest price & 1-day change for live ticker strip."""
    result = {}
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            hist = tk.history(period="5d")
            if len(hist) >= 2:
                cur = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2]
                chg = (cur - prev) / prev * 100
                result[t] = {"price": cur, "chg": chg}
        except Exception:
            pass
    return result

def color_return(val):
    """Pandas styler: colour cells by return magnitude."""
    if pd.isna(val):
        return "background-color: #1a2332; color: #555;"
    if val > 5:
        return f"background-color: #0a4a1a; color: #4cdd7a; font-weight:700;"
    elif val > 2:
        return f"background-color: #1a4a2a; color: #28a745;"
    elif val > 0:
        return f"background-color: #1a3a22; color: #7fc99d;"
    elif val > -2:
        return f"background-color: #3a1a1a; color: #e07070;"
    elif val > -5:
        return f"background-color: #4a1a1a; color: #dc3545;"
    else:
        return f"background-color: #5a0a0a; color: #ff6b6b; font-weight:700;"

def fmt(v):
    if pd.isna(v): return "—"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"

# ─────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────
st.html(f"""
<div class="hero-banner">
  <div class="hero-title">🌐 Global Index Monthly Return Tracker</div>
  <div class="hero-subtitle">
    Equity &amp; Commodity Indices · Americas · Europe · Asia-Pacific · Real-Time via Yahoo Finance
  </div>
  <div class="hero-badge">THE MOUNTAIN PATH – WORLD OF FINANCE</div>
</div>
""")

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.html(f'<div class="sidebar-logo">⛰ THE MOUNTAIN PATH<br><span style="font-size:0.7rem;color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">World of Finance</span></div>')

    st.markdown("### 📅 Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", value=date(2020, 1, 1), min_value=date(2010, 1, 1))
    with col2:
        end_date   = st.date_input("To",   value=date.today())

    st.markdown("---")
    st.markdown("### 🗂 Filter")

    asset_type = st.multiselect(
        "Asset Type",
        options=["Equity", "Commodity"],
        default=["Equity", "Commodity"]
    )

    region_opts = sorted(set(v["region"] for v in INDICES.values()))
    regions = st.multiselect(
        "Region",
        options=region_opts,
        default=region_opts
    )

    # Filter indices
    filtered_names = [
        name for name, meta in INDICES.items()
        if meta["type"] in asset_type and meta["region"] in regions
    ]
    all_names = list(INDICES.keys())

    st.markdown("### 📌 Select Indices")
    selected_names = st.multiselect(
        "Active Indices",
        options=all_names,
        default=filtered_names
    )

    st.markdown("---")
    st.markdown("### ⚙️ Display Options")
    show_heatmap   = st.checkbox("Monthly Heatmap",       value=True)
    show_bar       = st.checkbox("Annual Bar Chart",       value=True)
    show_line      = st.checkbox("Cumulative Return Chart",value=True)
    show_stats     = st.checkbox("Risk Statistics Table",  value=True)
    show_corr      = st.checkbox("Correlation Matrix",     value=False)

    st.markdown("---")
    refresh_btn = st.button("🔄  Refresh Live Data")
    if refresh_btn:
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.html(f"""
    <div style="font-size:0.7rem; color:{TEXT_MUTED}; text-align:center; -webkit-text-fill-color:{TEXT_MUTED};">
      Data sourced from Yahoo Finance.<br>For educational purposes only.
    </div>
    """)

# ─────────────────────────────────────────────
#  GUARD
# ─────────────────────────────────────────────
if not selected_names:
    st.warning("⚠️ Please select at least one index from the sidebar.")
    st.stop()

selected_tickers = [INDICES[n]["ticker"] for n in selected_names]

# ─────────────────────────────────────────────
#  FETCH DATA
# ─────────────────────────────────────────────
with st.spinner("📡 Fetching data from Yahoo Finance…"):
    try:
        returns_df = fetch_monthly_data(
            selected_tickers,
            str(start_date),
            str(end_date)
        )
        returns_df.columns = [TICKER_LIST.get(c, c) for c in returns_df.columns]
        # keep only selected names that have data
        returns_df = returns_df[[c for c in selected_names if c in returns_df.columns]]
    except Exception as e:
        st.error(f"❌ Data fetch error: {e}")
        st.stop()

if returns_df.empty or returns_df.dropna(how="all").empty:
    st.error("❌ No data returned. Please adjust the date range or selected indices.")
    st.stop()

# ─────────────────────────────────────────────
#  LIVE PRICE STRIP (top KPIs)
# ─────────────────────────────────────────────
latest_ret = returns_df.iloc[-1]       # most recent month
prev_ret   = returns_df.iloc[-2] if len(returns_df) >= 2 else latest_ret
ytd_ret    = ((1 + returns_df.dropna() / 100).prod() - 1) * 100 if not returns_df.empty else pd.Series()

best_idx  = latest_ret.idxmax()
worst_idx = latest_ret.idxmin()
best_val  = latest_ret.max()
worst_val = latest_ret.min()
avg_ret   = latest_ret.mean()
pos_count = (latest_ret > 0).sum()

sign_avg = "positive" if avg_ret >= 0 else "negative"
sign_best = "positive"
sign_worst = "negative"

st.html(f"""
<div class="section-header">📊 Latest Month Summary — {returns_df.index[-1]}</div>
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-label">Avg Monthly Return</div>
    <div class="metric-value {sign_avg}">{"+" if avg_ret>=0 else ""}{avg_ret:.2f}%</div>
    <div class="metric-sub">Across {len(selected_names)} indices</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Best Performer</div>
    <div class="metric-value {sign_best}">+{best_val:.2f}%</div>
    <div class="metric-sub">{best_idx}</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Worst Performer</div>
    <div class="metric-value {sign_worst}">{worst_val:.2f}%</div>
    <div class="metric-sub">{worst_idx}</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Positive Returns</div>
    <div class="metric-value neutral">{pos_count}/{len(selected_names)}</div>
    <div class="metric-sub">Indices in green</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Data Vintage</div>
    <div class="metric-value neutral" style="font-size:1.1rem;">{returns_df.index[-1]}</div>
    <div class="metric-sub">Last updated month</div>
  </div>
</div>
""")

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔥 Monthly Heatmap",
    "📈 Trend Charts",
    "📊 Annual Returns",
    "📉 Risk Statistics",
    "🔗 Correlation"
])

# ────────────────── TAB 1 : HEATMAP ──────────────────
with tab1:
    st.html('<div class="section-header">Monthly Return Heatmap — All Selected Indices</div>')

    # Pivot: rows = months, columns = index names
    heat_df = returns_df.copy().round(2)
    # Last N months selector
    n_months = st.slider("Show last N months", 6, min(60, len(heat_df)), min(24, len(heat_df)), key="hm_months")
    heat_df = heat_df.tail(n_months)

    # Plotly heatmap
    z_values = heat_df.values.T
    x_labels = list(heat_df.index)
    y_labels = list(heat_df.columns)

    fig_hm = go.Figure(go.Heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale=[
            [0.00, "#8b0000"], [0.20, "#dc3545"], [0.40, "#e8a0a0"],
            [0.50, "#2a3f5f"],
            [0.60, "#a0c8a0"], [0.80, "#28a745"], [1.00, "#004d00"]
        ],
        zmid=0,
        text=[[fmt(v) for v in row] for row in z_values],
        texttemplate="%{text}",
        textfont={"size": 9, "family": "JetBrains Mono"},
        colorbar=dict(
            title="Return %",
            titlefont=dict(color=GOLD),
            tickfont=dict(color=TEXT_MAIN),
            bgcolor=CARD_BG,
            outlinecolor=GOLD,
            thickness=14,
        ),
        hoverongaps=False,
        xgap=1, ygap=1,
    ))
    fig_hm.update_layout(
        height=max(500, len(y_labels) * 36 + 80),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_MAIN, family="Source Sans 3"),
        margin=dict(l=200, r=60, t=40, b=80),
        xaxis=dict(tickfont=dict(size=9), side="top",
                   tickangle=-45, gridcolor="rgba(255,255,255,0.03)"),
        yaxis=dict(tickfont=dict(size=10), autorange="reversed",
                   gridcolor="rgba(255,255,255,0.03)"),
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    # Raw table with styled cells
    st.html('<div class="section-header">Raw Monthly Returns Table</div>')
    styled = heat_df.style.applymap(color_return).format(fmt)
    styled = styled.set_properties(**{
        "font-family": "JetBrains Mono, monospace",
        "font-size": "12px",
        "text-align": "center",
        "border": "1px solid #1e3a5f",
    })
    styled = styled.set_table_styles([
        {"selector": "th",
         "props": [("background-color", DARK_BLUE), ("color", GOLD),
                   ("font-weight", "700"), ("font-size", "11px"),
                   ("border", f"1px solid {GOLD}"), ("text-align", "center")]},
    ])
    st.dataframe(styled, use_container_width=True, height=400)

    col_dl1, col_dl2 = st.columns([1, 5])
    with col_dl1:
        csv_data = heat_df.to_csv().encode("utf-8")
        st.download_button("⬇ Download CSV", csv_data, "monthly_returns.csv", "text/csv")


# ────────────────── TAB 2 : TREND CHARTS ──────────────────
with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.html('<div class="section-header">Cumulative Return (%)</div>')
        cum_df = (1 + returns_df.dropna() / 100).cumprod()
        cum_pct = (cum_df - 1) * 100
        fig_cum = go.Figure()
        colors_seq = px.colors.qualitative.Set2 + px.colors.qualitative.Pastel
        for i, col in enumerate(cum_pct.columns):
            fig_cum.add_trace(go.Scatter(
                x=cum_pct.index, y=cum_pct[col],
                name=col, mode="lines",
                line=dict(width=1.8, color=colors_seq[i % len(colors_seq)]),
                hovertemplate=f"<b>{col}</b><br>%{{x}}<br>Cumulative: %{{y:.1f}}%<extra></extra>"
            ))
        fig_cum.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_cum.update_layout(
            height=420, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_MAIN),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
            margin=dict(l=50, r=20, t=20, b=40),
            hovermode="x unified",
        )
        st.plotly_chart(fig_cum, use_container_width=True)

    with col_b:
        st.html('<div class="section-header">Rolling 3-Month Return (%)</div>')
        roll3 = returns_df.rolling(3).sum()
        fig_roll = go.Figure()
        for i, col in enumerate(roll3.columns):
            fig_roll.add_trace(go.Scatter(
                x=roll3.index, y=roll3[col],
                name=col, mode="lines",
                line=dict(width=1.8, color=colors_seq[i % len(colors_seq)]),
                hovertemplate=f"<b>{col}</b><br>%{{x}}<br>3M Return: %{{y:.1f}}%<extra></extra>"
            ))
        fig_roll.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_roll.update_layout(
            height=420, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_MAIN),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
            margin=dict(l=50, r=20, t=20, b=40),
            hovermode="x unified",
        )
        st.plotly_chart(fig_roll, use_container_width=True)

    # Waterfall for latest month
    st.html('<div class="section-header">Latest Month Return — Ranked Bar</div>')
    latest_sorted = latest_ret.dropna().sort_values(ascending=True)
    bar_colors = [GREEN if v >= 0 else RED for v in latest_sorted.values]
    fig_bar_latest = go.Figure(go.Bar(
        x=latest_sorted.values,
        y=latest_sorted.index,
        orientation="h",
        marker_color=bar_colors,
        text=[fmt(v) for v in latest_sorted.values],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=10, color=TEXT_MAIN),
        hovertemplate="<b>%{y}</b><br>Return: %{x:.2f}%<extra></extra>",
    ))
    fig_bar_latest.add_vline(x=0, line_color="rgba(255,255,255,0.3)", line_dash="solid", line_width=1)
    fig_bar_latest.update_layout(
        height=max(400, len(latest_sorted) * 30 + 60),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_MAIN, family="Source Sans 3"),
        margin=dict(l=20, r=80, t=20, b=40),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
        yaxis=dict(gridcolor="none"),
        bargap=0.3,
    )
    st.plotly_chart(fig_bar_latest, use_container_width=True)


# ────────────────── TAB 3 : ANNUAL RETURNS ──────────────────
with tab3:
    st.html('<div class="section-header">Annual Returns by Index (%)</div>')
    # Add year column
    rd_copy = returns_df.copy()
    rd_copy.index = pd.PeriodIndex(rd_copy.index, freq="M")
    annual = rd_copy.groupby(rd_copy.index.year).apply(
        lambda df: ((1 + df / 100).prod() - 1) * 100
    )
    annual.index.name = "Year"

    fig_annual = go.Figure()
    for i, idx_name in enumerate(annual.columns):
        fig_annual.add_trace(go.Bar(
            name=idx_name,
            x=annual.index.astype(str),
            y=annual[idx_name].round(2),
            hovertemplate=f"<b>{idx_name}</b><br>Year: %{{x}}<br>Return: %{{y:.2f}}%<extra></extra>"
        ))
    fig_annual.update_layout(
        barmode="group",
        height=520,
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_MAIN, family="Source Sans 3"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
        xaxis=dict(title="Year", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title="Annual Return (%)", gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
        margin=dict(l=60, r=20, t=20, b=40),
    )
    st.plotly_chart(fig_annual, use_container_width=True)

    # Annual table
    st.html('<div class="section-header">Annual Return Table</div>')
    ann_styled = annual.round(2).style.applymap(color_return).format(fmt)
    ann_styled = ann_styled.set_properties(**{
        "font-family": "JetBrains Mono, monospace",
        "font-size": "12px", "text-align": "center",
        "border": "1px solid #1e3a5f",
    }).set_table_styles([{
        "selector": "th",
        "props": [("background-color", DARK_BLUE), ("color", GOLD),
                  ("font-weight", "700"), ("font-size", "11px"),
                  ("border", f"1px solid {GOLD}"), ("text-align", "center")]
    }])
    st.dataframe(ann_styled, use_container_width=True)


# ────────────────── TAB 4 : RISK STATISTICS ──────────────────
with tab4:
    st.html('<div class="section-header">Risk & Return Statistics — Full Period</div>')

    stats = pd.DataFrame(index=returns_df.columns)
    clean = returns_df.dropna()
    stats["Avg Monthly Ret (%)"]    = clean.mean().round(3)
    stats["Ann. Return (%)"]        = (((1 + clean.mean()/100)**12)-1)*100
    stats["Monthly Volatility (%)"] = clean.std().round(3)
    stats["Ann. Volatility (%)"]    = (clean.std() * np.sqrt(12)).round(3)
    stats["Sharpe Ratio"]           = ((stats["Ann. Return (%)"] - 4.5) / stats["Ann. Volatility (%)"]).round(3)
    stats["Max Monthly Gain (%)"]   = clean.max().round(3)
    stats["Max Monthly Loss (%)"]   = clean.min().round(3)
    stats["Skewness"]               = clean.skew().round(3)
    stats["Kurtosis"]               = clean.kurt().round(3)
    stats["Positive Months"]        = (clean > 0).sum()
    stats["Hit Rate (%)"]           = ((clean > 0).sum() / len(clean) * 100).round(1)
    stats["VaR 95% (Monthly %)"]    = clean.quantile(0.05).round(3)
    stats["CVaR 95% (Monthly %)"]   = clean[clean.le(clean.quantile(0.05))].mean().round(3)

    def color_stat(val, col):
        if col in ["Avg Monthly Ret (%)", "Ann. Return (%)", "Sharpe Ratio",
                   "Max Monthly Gain (%)", "Hit Rate (%)"]:
            if pd.isna(val): return ""
            return f"color: {GREEN}; font-weight:700;" if val > 0 else f"color: {RED};"
        if col in ["Max Monthly Loss (%)", "VaR 95% (Monthly %)", "CVaR 95% (Monthly %)"]:
            if pd.isna(val): return ""
            return f"color: {RED}; font-weight:700;" if val < 0 else f"color: {GREEN};"
        return ""

    st.dataframe(
        stats.style.apply(
            lambda col: [color_stat(v, col.name) for v in col], axis=0
        ).format({
            c: "{:.2f}" for c in stats.select_dtypes("float").columns
        }).set_properties(**{
            "font-family": "JetBrains Mono, monospace",
            "font-size": "11px", "text-align": "right",
            "border": "1px solid #1e3a5f",
        }).set_table_styles([{
            "selector": "th",
            "props": [("background-color", DARK_BLUE), ("color", GOLD),
                      ("font-weight", "700"), ("font-size", "11px"),
                      ("border", f"1px solid {GOLD}"), ("text-align", "center")]
        }]),
        use_container_width=True, height=480
    )

    # Sharpe ratio bar
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.html('<div class="section-header">Sharpe Ratio Comparison</div>')
        sh = stats["Sharpe Ratio"].sort_values(ascending=True)
        fig_sh = go.Figure(go.Bar(
            x=sh.values, y=sh.index, orientation="h",
            marker_color=[GREEN if v >= 0 else RED for v in sh.values],
            text=[f"{v:.2f}" for v in sh.values], textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9),
        ))
        fig_sh.update_layout(
            height=max(380, len(sh)*28+60),
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_MAIN), margin=dict(l=10, r=60, t=20, b=40),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="none"),
        )
        st.plotly_chart(fig_sh, use_container_width=True)

    with col_s2:
        st.html('<div class="section-header">Annualised Risk vs Return</div>')
        fig_rv = go.Figure()
        for idx in stats.index:
            x_val = stats.loc[idx, "Ann. Volatility (%)"]
            y_val = stats.loc[idx, "Ann. Return (%)"]
            fig_rv.add_trace(go.Scatter(
                x=[x_val], y=[y_val], mode="markers+text",
                name=idx,
                text=[idx[:12]], textposition="top center",
                textfont=dict(size=8),
                marker=dict(size=12, symbol="circle",
                            color=GREEN if y_val >= 0 else RED,
                            line=dict(width=1, color=GOLD)),
                hovertemplate=f"<b>{idx}</b><br>Ann Return: {y_val:.1f}%<br>Ann Vol: {x_val:.1f}%<extra></extra>"
            ))
        fig_rv.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_rv.update_layout(
            height=max(380, 420),
            showlegend=False,
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_MAIN),
            xaxis=dict(title="Annual Volatility (%)", gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
            yaxis=dict(title="Annual Return (%)", gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
            margin=dict(l=50, r=20, t=20, b=50),
        )
        st.plotly_chart(fig_rv, use_container_width=True)

    # Download stats
    csv_stats = stats.to_csv().encode("utf-8")
    st.download_button("⬇ Download Risk Statistics CSV", csv_stats, "risk_stats.csv", "text/csv")


# ────────────────── TAB 5 : CORRELATION ──────────────────
with tab5:
    st.html('<div class="section-header">Correlation Matrix — Monthly Returns</div>')
    corr = returns_df.dropna().corr().round(3)

    fig_corr = go.Figure(go.Heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.index),
        colorscale=[
            [0.0, "#8b0000"], [0.3, "#dc3545"], [0.5, "#2a3f5f"],
            [0.7, "#1a6b1a"], [1.0, "#004d00"]
        ],
        zmin=-1, zmax=1, zmid=0,
        text=corr.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 9, "family": "JetBrains Mono"},
        colorbar=dict(
            title="Correlation",
            titlefont=dict(color=GOLD),
            tickfont=dict(color=TEXT_MAIN),
            bgcolor=CARD_BG,
            outlinecolor=GOLD,
            thickness=14,
        ),
        xgap=1, ygap=1,
    ))
    fig_corr.update_layout(
        height=max(500, len(corr)*36+80),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_MAIN, family="Source Sans 3"),
        margin=dict(l=180, r=60, t=40, b=120),
        xaxis=dict(tickfont=dict(size=9), tickangle=-45, side="bottom"),
        yaxis=dict(tickfont=dict(size=10), autorange="reversed"),
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.html('<div class="section-header">Highly Correlated Pairs ( |ρ| &gt; 0.75 )</div>')
    pairs = []
    cols = list(corr.columns)
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            v = corr.iloc[i,j]
            if abs(v) > 0.75:
                pairs.append({"Index A": cols[i], "Index B": cols[j], "Correlation": round(v,3)})
    if pairs:
        pairs_df = pd.DataFrame(pairs).sort_values("Correlation", ascending=False)
        st.dataframe(pairs_df, use_container_width=True, hide_index=True)
    else:
        st.info("No pairs with |ρ| > 0.75 in the selected universe.")


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.html(f"""
<div class="footer">
  <div class="footer-name">Prof. V. Ravichandran &nbsp;|&nbsp;
    28+ Years Corporate Finance &amp; Banking Experience &nbsp;|&nbsp; 10+ Years Academic Excellence
  </div>
  <div class="footer-links">
    <a href="https://www.linkedin.com/in/trichyravis" target="_blank">🔗 LinkedIn</a>
    <a href="https://github.com/trichyravis" target="_blank">💻 GitHub</a>
    <span style="color:{TEXT_MUTED}; font-size:0.75rem; margin-left:18px; -webkit-text-fill-color:{TEXT_MUTED};">
      Visiting Faculty: NMIMS Bangalore · BITS Pilani · RV University · Goa Institute of Management
    </span>
  </div>
</div>
""")
