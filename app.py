
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
/* Sidebar text — targeted, not blanket * override */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] div[class*="markdown"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: {TEXT_MAIN} !important;
    -webkit-text-fill-color: {TEXT_MAIN} !important;
}}
/* Widget labels in sidebar — light blue like other label text */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] [data-testid="stDateInput"] [data-testid="stWidgetLabel"] p {{
    color: {LIGHT_BLUE} !important;
    -webkit-text-fill-color: {LIGHT_BLUE} !important;
    font-weight: 600 !important;
    opacity: 1 !important;
    visibility: visible !important;
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

/* Widget label universal fix — covers all inputs in sidebar columns */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stWidgetLabel"] label,
[data-testid="stDateInput"] label,
[data-testid="stDateInput"] p,
[data-testid="stDateInput"] span,
[data-testid="stDateInput"] div[class*="label"],
.stDateInput > label,
.stDateInput > div > label,
div[class*="stDateInput"] label {{
    color: {LIGHT_BLUE} !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: {LIGHT_BLUE} !important;
    opacity: 1 !important;
    visibility: visible !important;
}}
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
    start_date = st.date_input("📅 From", value=date(2020, 1, 1), min_value=date(2010, 1, 1))
    end_date   = st.date_input("📅 To",   value=date.today())

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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🔥 Monthly Heatmap",
    "📈 Trend Charts",
    "📊 Annual Returns",
    "📉 Risk Statistics",
    "🔗 Correlation",
    "🏆 Rankings",
    "📖 Methodology"
])

# ────────────────── TAB 1 : HEATMAP ──────────────────
with tab1:
    st.html('<div class="section-header">Monthly Return Heatmap — All Selected Indices</div>')

    # Pivot: rows = months, columns = index names
    heat_df = returns_df.copy().round(2)
    # Last N months selector — guard against too few rows
    _total   = len(heat_df)
    _min_val = min(6, _total)
    _max_val = max(_min_val, min(60, _total))
    _def_val = min(24, _max_val)
    if _min_val < _max_val:
        n_months = st.slider("Show last N months", _min_val, _max_val, _def_val, key="hm_months")
    else:
        n_months = _total
        st.info(f"Showing all {_total} available months.")
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
            title=dict(text="Return %", font=dict(color=GOLD)),
            tickfont=dict(color=TEXT_MAIN),
            thickness=14,
            outlinewidth=0,
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
    styled = heat_df.style.map(color_return).format(fmt)
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
        width=0.6,
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
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_bar_latest, use_container_width=True)


# ────────────────── TAB 3 : ANNUAL RETURNS ──────────────────
with tab3:
    st.html('<div class="section-header">Annual Returns by Index (%)</div>')
    # Add year column
    rd_copy = returns_df.copy()
    rd_copy.index = pd.PeriodIndex(rd_copy.index, freq="M")
    annual = rd_copy.groupby(rd_copy.index.year).apply(
        lambda df: ((1 + df / 100).prod() - 1) * 100, include_groups=False
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
    ann_styled = annual.round(2).style.map(color_return).format(fmt)
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
    var_95 = clean.quantile(0.05)
    cvar_95 = pd.Series(
        {col: clean[col][clean[col] <= var_95[col]].mean() for col in clean.columns},
        name="CVaR"
    ).round(3)
    stats["VaR 95% (Monthly %)"]    = var_95.round(3)
    stats["CVaR 95% (Monthly %)"]   = cvar_95

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
            yaxis=dict(showgrid=False),
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
            title=dict(text="Correlation", font=dict(color=GOLD)),
            tickfont=dict(color=TEXT_MAIN),
            thickness=14,
            outlinewidth=0,
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



# ────────────────── TAB 6 : RANKINGS ──────────────────
with tab6:
    st.html('<div class="section-header">🏆 Index Rankings — Return & Risk Scorecard</div>')

    clean = returns_df.dropna()

    # ── Build rankings dataframe ──
    rank_df = pd.DataFrame(index=returns_df.columns)
    rank_df["Avg Monthly Ret (%)"]  = clean.mean().round(3)
    rank_df["Ann. Return (%)"]      = (((1 + clean.mean()/100)**12)-1)*100
    rank_df["Ann. Volatility (%)"]  = (clean.std() * np.sqrt(12)).round(3)
    rank_df["Sharpe Ratio"]         = ((rank_df["Ann. Return (%)"] - 4.5)
                                        / rank_df["Ann. Volatility (%)"]).round(3)
    var95 = clean.quantile(0.05)
    rank_df["VaR 95% (%)"]          = var95.round(3)
    rank_df["CVaR 95% (%)"]         = pd.Series(
        {c: clean[c][clean[c] <= var95[c]].mean() for c in clean.columns}
    ).round(3)
    rank_df["Hit Rate (%)"]         = ((clean > 0).sum() / len(clean) * 100).round(1)
    rank_df["Max Monthly Loss (%)"] = clean.min().round(3)

    # ── Ordinal ranks (1 = best) ──
    rank_df["Rank: Return"]    = rank_df["Ann. Return (%)"].rank(ascending=False).astype(int)
    rank_df["Rank: Volatility"]= rank_df["Ann. Volatility (%)"].rank(ascending=True).astype(int)   # lower = better
    rank_df["Rank: Sharpe"]    = rank_df["Sharpe Ratio"].rank(ascending=False).astype(int)
    rank_df["Rank: VaR"]       = rank_df["VaR 95% (%)"].rank(ascending=False).astype(int)          # less negative = better
    rank_df["Rank: Hit Rate"]  = rank_df["Hit Rate (%)"].rank(ascending=False).astype(int)

    # ── Composite score: average of all ranks (lower = better overall) ──
    rank_cols = ["Rank: Return","Rank: Volatility","Rank: Sharpe","Rank: VaR","Rank: Hit Rate"]
    rank_df["Composite Score"] = rank_df[rank_cols].mean(axis=1).round(2)
    rank_df["Overall Rank"]    = rank_df["Composite Score"].rank(ascending=True).astype(int)
    rank_df = rank_df.sort_values("Overall Rank")

    # ── Medal emojis ──
    def medal(r):
        return {1:"🥇", 2:"🥈", 3:"🥉"}.get(r, f"#{r}")

    # ── Summary cards: Top 3 overall ──
    st.html('<div class="section-header">🎖 Overall Top Performers</div>')
    top3 = rank_df.head(3)
    card_cols = st.columns(3)
    for i, (idx_name, row) in enumerate(top3.iterrows()):
        sign = "positive" if row["Ann. Return (%)"] >= 0 else "negative"
        ret_str = f'{"+" if row["Ann. Return (%)"]>=0 else ""}{row["Ann. Return (%)"]:.1f}%'
        with card_cols[i]:
            st.html(f"""
            <div class="metric-card" style="border-color:{GOLD};">
              <div class="metric-label">{medal(i+1)} Overall Rank #{i+1}</div>
              <div class="metric-value neutral" style="font-size:1.1rem; white-space:normal;">{idx_name}</div>
              <div class="metric-sub" style="margin-top:8px;">
                Ann Return: <span style="color:{'#28a745' if row['Ann. Return (%)']>=0 else '#dc3545'}; -webkit-text-fill-color:{'#28a745' if row['Ann. Return (%)']>=0 else '#dc3545'}; font-weight:700;">{ret_str}</span><br>
                Sharpe: <span style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-weight:700;">{row['Sharpe Ratio']:.2f}</span><br>
                Volatility: {row['Ann. Volatility (%)']:.1f}% &nbsp;|&nbsp; Hit Rate: {row['Hit Rate (%)']:.0f}%
              </div>
            </div>""")

    # ── Full rankings table ──
    st.html('<div class="section-header">📋 Full Rankings Table</div>')

    display_cols = [
        "Overall Rank", "Ann. Return (%)", "Ann. Volatility (%)", "Sharpe Ratio",
        "VaR 95% (%)", "CVaR 95% (%)", "Hit Rate (%)", "Max Monthly Loss (%)",
        "Rank: Return", "Rank: Volatility", "Rank: Sharpe", "Rank: VaR", "Rank: Hit Rate",
        "Composite Score"
    ]
    disp_df = rank_df[display_cols].copy()

    def style_rank_row(val, col):
        if col == "Overall Rank":
            if val == 1:   return f"background-color:#b8860b; color:#000; font-weight:900;"
            if val == 2:   return f"background-color:#808080; color:#000; font-weight:700;"
            if val == 3:   return f"background-color:#8b4513; color:#fff; font-weight:700;"
            return ""
        if col in ["Ann. Return (%)", "Sharpe Ratio", "Hit Rate (%)"]:
            if pd.isna(val): return ""
            return f"color:{GREEN}; font-weight:700;" if val > 0 else f"color:{RED};"
        if col in ["Ann. Volatility (%)", "VaR 95% (%)", "CVaR 95% (%)", "Max Monthly Loss (%)"]:
            if pd.isna(val): return ""
            return f"color:{RED};" if val < 0 else f"color:{GREEN};"
        if col in ["Rank: Return","Rank: Volatility","Rank: Sharpe","Rank: VaR","Rank: Hit Rate","Composite Score"]:
            if pd.isna(val): return ""
            n = len(rank_df)
            if val <= max(1, n*0.2):  return f"color:{GREEN}; font-weight:700;"
            if val >= n*0.8:           return f"color:{RED};"
            return f"color:{GOLD};"
        return ""

    styled_rank = (
        disp_df.style
        .apply(lambda col: [style_rank_row(v, col.name) for v in col], axis=0)
        .format({
            "Ann. Return (%)":      "{:+.2f}%",
            "Ann. Volatility (%)":  "{:.2f}%",
            "Sharpe Ratio":         "{:.3f}",
            "VaR 95% (%)":          "{:.2f}%",
            "CVaR 95% (%)":         "{:.2f}%",
            "Hit Rate (%)":         "{:.1f}%",
            "Max Monthly Loss (%)": "{:.2f}%",
            "Composite Score":      "{:.2f}",
            "Overall Rank":         "#{:.0f}",
            "Rank: Return":         "#{:.0f}",
            "Rank: Volatility":     "#{:.0f}",
            "Rank: Sharpe":         "#{:.0f}",
            "Rank: VaR":            "#{:.0f}",
            "Rank: Hit Rate":       "#{:.0f}",
        })
        .set_properties(**{
            "font-family": "JetBrains Mono, monospace",
            "font-size": "11px", "text-align": "center",
            "border": f"1px solid {CARD_BG}",
        })
        .set_table_styles([{"selector": "th",
                            "props": [("background-color", DARK_BLUE),
                                      ("color", GOLD), ("font-weight", "700"),
                                      ("font-size", "11px"), ("text-align", "center"),
                                      ("border", f"1px solid {GOLD}")]}])
    )
    st.dataframe(styled_rank, use_container_width=True, height=500)

    # ── Individual dimension rankings ──
    st.html('<div class="section-header">📊 Rankings by Individual Dimension</div>')

    dim_tabs = st.tabs([
        "📈 Return Rank", "📉 Risk (Vol) Rank", "⚖️ Sharpe Rank",
        "🛡 VaR Rank", "🎯 Hit Rate Rank"
    ])

    dim_configs = [
        ("Rank: Return",     "Ann. Return (%)",     "Annual Return",     True,  "{:+.2f}%"),
        ("Rank: Volatility", "Ann. Volatility (%)", "Ann. Volatility",   False, "{:.2f}%"),
        ("Rank: Sharpe",     "Sharpe Ratio",        "Sharpe Ratio",      True,  "{:.3f}"),
        ("Rank: VaR",        "VaR 95% (%)",         "VaR 95%",           False, "{:.2f}%"),
        ("Rank: Hit Rate",   "Hit Rate (%)",        "Hit Rate",          True,  "{:.1f}%"),
    ]

    for dtab, (rank_col, val_col, label, higher_better, val_fmt) in zip(dim_tabs, dim_configs):
        with dtab:
            sorted_dim = rank_df.sort_values(rank_col)
            vals       = sorted_dim[val_col]
            bar_colors = []
            for i, v in enumerate(vals):
                if i == 0:   bar_colors.append(GOLD)
                elif i == 1: bar_colors.append("#C0C0C0")
                elif i == 2: bar_colors.append("#CD7F32")
                elif i < len(vals)//3: bar_colors.append(GREEN)
                elif i > 2*len(vals)//3: bar_colors.append(RED)
                else: bar_colors.append(LIGHT_BLUE)

            fig_dim = go.Figure(go.Bar(
                x=vals.values,
                y=[f"{medal(int(r))} {n}" for n, r in zip(sorted_dim.index, sorted_dim[rank_col])],
                orientation="h",
                marker_color=bar_colors,
                width=0.6,
                text=[val_fmt.format(v) for v in vals.values],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=10, color=TEXT_MAIN),
                hovertemplate=f"<b>%{{y}}</b><br>{label}: %{{x:.2f}}<extra></extra>",
            ))
            fig_dim.add_vline(x=0, line_color="rgba(255,255,255,0.2)", line_width=1)
            fig_dim.update_layout(
                height=max(400, len(sorted_dim)*32+80),
                paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
                font=dict(color=TEXT_MAIN, family="Source Sans 3"),
                margin=dict(l=10, r=90, t=30, b=40),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(showgrid=False, autorange="reversed"),
                showlegend=False,
                title=dict(
                    text=f"Ranked by {label} ({'Higher = Better' if higher_better else 'Lower = Better'})",
                    font=dict(color=GOLD, size=13), x=0.01
                ),
            )
            st.plotly_chart(fig_dim, use_container_width=True)

    # ── Radar / spider chart: top 5 overall ──
    st.html('<div class="section-header">🕸 Risk-Return Radar — Top 5 Overall</div>')

    top5 = rank_df.head(min(5, len(rank_df)))
    radar_metrics = ["Rank: Return","Rank: Volatility","Rank: Sharpe","Rank: VaR","Rank: Hit Rate"]
    radar_labels  = ["Return","Low Vol","Sharpe","Low VaR","Hit Rate"]
    n_indices = len(rank_df)

    fig_radar = go.Figure()
    radar_colors = [GOLD, LIGHT_BLUE, GREEN, "#FF6B6B", "#9B59B6"]
    for i, (idx_name, row) in enumerate(top5.iterrows()):
        # Invert ranks so that rank 1 = full outer ring (score = n, rank n = score 1)
        scores = [n_indices + 1 - row[r] for r in radar_metrics]
        scores_closed = scores + [scores[0]]
        labels_closed = radar_labels + [radar_labels[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=scores_closed,
            theta=labels_closed,
            fill="toself",
            name=idx_name[:20],
            line=dict(color=radar_colors[i % len(radar_colors)], width=2),
            fillcolor=radar_colors[i % len(radar_colors)].replace("#", "rgba(").rstrip(")") if False else "rgba(0,0,0,0)",
            opacity=0.85,
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor=CARD_BG,
            radialaxis=dict(
                visible=True, range=[0, n_indices],
                tickfont=dict(size=8, color=TEXT_MUTED),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.15)",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=GOLD, family="Source Sans 3"),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor=GOLD,
            ),
        ),
        paper_bgcolor=CARD_BG,
        font=dict(color=TEXT_MAIN),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=TEXT_MAIN)),
        height=480,
        margin=dict(l=60, r=60, t=60, b=60),
        title=dict(
            text="Higher score = Better rank on each dimension",
            font=dict(color=TEXT_MUTED, size=11), x=0.5
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ── How-to-read legend ──
    col_leg1, col_leg2 = st.columns(2)
    with col_leg1:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:16px 20px;">
          <div class="metric-label" style="margin-bottom:10px;">🏅 Ranking Methodology</div>
          <div class="metric-sub" style="line-height:1.8;">
            <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">Return Rank</b> — Ann. return (higher = better)<br>
            <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">Volatility Rank</b> — Ann. vol (lower = better)<br>
            <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">Sharpe Rank</b> — Risk-adj return (higher = better)<br>
            <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">VaR Rank</b> — 95% VaR (less negative = better)<br>
            <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">Hit Rate Rank</b> — % positive months (higher = better)
          </div>
        </div>""")
    with col_leg2:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:16px 20px;">
          <div class="metric-label" style="margin-bottom:10px;">🧮 Composite Score</div>
          <div class="metric-sub" style="line-height:1.8;">
            Simple average of all 5 dimension ranks.<br>
            <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">Lower composite = better overall rank.</b><br><br>
            Rank #1 on a dimension = score of 1.<br>
            All dimensions are equally weighted.<br>
            Risk-free rate assumed <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">4.5%</b> for Sharpe.
          </div>
        </div>""")

    csv_rank = rank_df[display_cols].to_csv().encode()
    st.download_button("⬇ Download Rankings CSV", csv_rank, "index_rankings.csv", "text/csv")



# ────────────────── TAB 7 : METHODOLOGY ──────────────────
with tab7:
    st.html('''<div class="section-header">📖 Methodology & Technical Reference</div>''')

    st.html(f"""
    <div class="metric-card" style="text-align:left; padding:20px 28px; margin-bottom:18px;">
      <div style="font-family:'Cinzel',serif; font-size:1.1rem; color:{GOLD};
                  -webkit-text-fill-color:{GOLD}; margin-bottom:10px; font-weight:700;">
        🌐 About This Dashboard
      </div>
      <div class="metric-sub" style="line-height:1.9; font-size:0.9rem;">
        This dashboard tracks <b style="color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">monthly returns</b>
        for 20 global equity and commodity indices sourced live from
        <b style="color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">Yahoo Finance</b> via the
        <code style="background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px;">yfinance</code> library.
        All return series are computed from <b>month-end adjusted closing prices</b>.
        Data is cached for 1 hour (<code style="background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px;">ttl=3600s</code>)
        and can be force-refreshed via the sidebar button.<br><br>
        Risk-free rate assumed throughout: <b style="color:{GOLD};-webkit-text-fill-color:{GOLD};">4.5% per annum</b>
        (approximate Indian T-Bill / short-term sovereign rate).
      </div>
    </div>
    """)

    # ── Section 1: Return Calculations ──
    st.html('''<div class="section-header">📐 Section 1 — Return Calculations</div>''')

    col1, col2 = st.columns(2)
    with col1:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Monthly Simple Return</div>
          <div class="metric-sub" style="line-height:1.8;">
            The percentage change in the adjusted closing price from the last
            trading day of month <i>t−1</i> to the last trading day of month <i>t</i>.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            R<sub>t</sub> = (P<sub>t</sub> − P<sub>t−1</sub>) / P<sub>t−1</sub> × 100
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            P<sub>t</sub> = Month-end adjusted close price<br>
            Computed via <code>pct_change()</code> after <code>resample("ME").last()</code>
          </div>
        </div>""")

        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px; margin-top:14px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Annualised Return</div>
          <div class="metric-sub" style="line-height:1.8;">
            Compounds the average monthly return to an annual figure using
            geometric compounding — more accurate than simple multiplication by 12.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            R<sub>ann</sub> = (1 + R̄<sub>monthly</sub>/100)<sup>12</sup> − 1
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            R̄<sub>monthly</sub> = arithmetic mean of monthly returns<br>
            Result expressed as a percentage
          </div>
        </div>""")

    with col2:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Cumulative Return</div>
          <div class="metric-sub" style="line-height:1.8;">
            Tracks ₹1 invested at the start of the period, compounding each
            monthly return. Reveals the true growth trajectory including
            path dependency and volatility drag.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            CumRet<sub>T</sub> = ∏(1 + R<sub>t</sub>/100) − 1
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Implemented via <code>cumprod()</code> on (1 + R/100)
          </div>
        </div>""")

        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px; margin-top:14px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Annual Return (Calendar Year)</div>
          <div class="metric-sub" style="line-height:1.8;">
            Compounds all 12 monthly returns within each calendar year.
            Partial years at the start and end of the selected date range
            are included with whatever months are available.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            R<sub>year</sub> = ∏<sub>t∈year</sub>(1 + R<sub>t</sub>/100) − 1
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Grouped by <code>index.year</code> via pandas <code>groupby</code>
          </div>
        </div>""")

    # ── Section 2: Volatility ──
    st.html('''<div class="section-header">📐 Section 2 — Volatility & Dispersion</div>''')

    col3, col4 = st.columns(2)
    with col3:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Monthly Volatility (Std Dev)</div>
          <div class="metric-sub" style="line-height:1.8;">
            Sample standard deviation of monthly returns. Measures the
            average dispersion of returns around the mean — the most
            widely used measure of total risk.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            σ<sub>m</sub> = √[ Σ(R<sub>t</sub> − R̄)² / (n−1) ]
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Uses Bessel correction (n−1 denominator) — sample std dev
          </div>
        </div>""")

    with col4:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Annualised Volatility</div>
          <div class="metric-sub" style="line-height:1.8;">
            Scales monthly volatility to an annual figure using the
            square-root-of-time rule — valid under i.i.d. return assumptions.
            Standard convention in risk management and portfolio theory.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            σ<sub>ann</sub> = σ<sub>m</sub> × √12
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            √12 ≈ 3.464 · Assumes independent monthly returns<br>
            For daily data the multiplier would be √252
          </div>
        </div>""")

    # ── Section 3: Risk-Adjusted Metrics ──
    st.html('''<div class="section-header">📐 Section 3 — Risk-Adjusted Performance</div>''')

    col5, col6 = st.columns(2)
    with col5:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Sharpe Ratio</div>
          <div class="metric-sub" style="line-height:1.8;">
            Measures excess return earned per unit of total risk (volatility).
            The most widely used risk-adjusted performance metric in finance.
            A Sharpe above 1.0 is considered good; above 2.0 is excellent.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            S = (R<sub>ann</sub> − R<sub>f</sub>) / σ<sub>ann</sub>
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            R<sub>f</sub> = 4.5% p.a. (Indian short-term sovereign rate)<br>
            Higher Sharpe = better risk-adjusted return
          </div>
        </div>""")

        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px; margin-top:14px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Hit Rate (%)</div>
          <div class="metric-sub" style="line-height:1.8;">
            The percentage of months in which the index delivered a
            positive return. A simple, intuitive measure of directional
            consistency — independent of return magnitude.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            Hit Rate = (# months R<sub>t</sub> &gt; 0) / n × 100
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            &gt; 55% is generally considered consistent<br>
            Does not account for magnitude of gains vs losses
          </div>
        </div>""")

    with col6:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Skewness</div>
          <div class="metric-sub" style="line-height:1.8;">
            Measures the asymmetry of the return distribution.
            <b style="color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">Positive skew</b>
            (right tail) implies occasional large gains.
            <b style="color:{RED};-webkit-text-fill-color:{RED};">Negative skew</b>
            (left tail) implies occasional large losses — dangerous for risk management.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            Skew = E[(R − μ)³] / σ³
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Normal distribution: Skew = 0<br>
            Most equity indices exhibit negative skew
          </div>
        </div>""")

        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px; margin-top:14px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Excess Kurtosis</div>
          <div class="metric-sub" style="line-height:1.8;">
            Measures the "fat-tailedness" of the return distribution relative
            to a normal distribution. High positive kurtosis (leptokurtosis)
            means more extreme outcomes than normality predicts — a critical
            consideration for VaR model validation.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            Kurt<sub>excess</sub> = E[(R − μ)⁴]/σ⁴ − 3
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Normal distribution: Kurt = 0<br>
            Equity markets typically exhibit Kurt &gt; 0 (fat tails)
          </div>
        </div>""")

    # ── Section 4: Tail Risk ──
    st.html('''<div class="section-header">📐 Section 4 — Tail Risk: VaR & CVaR</div>''')

    col7, col8 = st.columns(2)
    with col7:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Value at Risk — VaR (95%)</div>
          <div class="metric-sub" style="line-height:1.8;">
            The <b>worst monthly loss</b> we would not expect to exceed with 95% confidence.
            Implemented here using the <b>Historical Simulation</b> method — no
            distributional assumption is required; the empirical return series
            directly determines the threshold.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            VaR<sub>95%</sub> = 5th percentile of R<sub>t</sub>
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Interpretation: "In 95% of months, the loss will not exceed VaR"<br>
            Implemented via <code>quantile(0.05)</code>
          </div>
        </div>""")

    with col8:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">CVaR / Expected Shortfall (95%)</div>
          <div class="metric-sub" style="line-height:1.8;">
            The <b>average loss in the worst 5% of months</b>. CVaR is a coherent
            risk measure (unlike VaR) and satisfies sub-additivity — meaning
            diversification always reduces CVaR. Preferred by Basel III / FRTB
            over VaR for internal model approaches.
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            CVaR<sub>95%</sub> = E[ R<sub>t</sub> | R<sub>t</sub> ≤ VaR<sub>95%</sub> ]
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Always ≤ VaR (more conservative) · Captures tail shape<br>
            Preferred by SEBI stress-testing and Basel FRTB frameworks
          </div>
        </div>""")

    # ── Section 5: Correlation ──
    st.html('''<div class="section-header">📐 Section 5 — Correlation Analysis</div>''')

    col9, col10 = st.columns(2)
    with col9:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Pearson Correlation Matrix</div>
          <div class="metric-sub" style="line-height:1.8;">
            Pairwise linear correlation between monthly return series.
            The matrix is symmetric with diagonal = 1.
            Computed on the intersection of available months (listwise deletion
            of NaN rows via <code>dropna()</code>).
          </div>
          <div style="font-family:'JetBrains Mono',monospace; background:rgba(0,0,0,0.35);
                      padding:10px 14px; border-radius:6px; margin-top:12px;
                      border-left:3px solid {GOLD}; font-size:0.85rem; color:{TEXT_MAIN};
                      -webkit-text-fill-color:{TEXT_MAIN};">
            ρ<sub>ij</sub> = Cov(R<sub>i</sub>, R<sub>j</sub>) / (σ<sub>i</sub> · σ<sub>j</sub>)
          </div>
          <div class="metric-sub" style="margin-top:10px; font-size:0.78rem;">
            Range: −1 (perfect inverse) to +1 (perfect co-movement)<br>
            |ρ| &gt; 0.75 flagged as highly correlated pairs
          </div>
        </div>""")

    with col10:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:18px 22px;">
          <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                      font-size:0.95rem; margin-bottom:12px;">Diversification Insight</div>
          <div class="metric-sub" style="line-height:1.8;">
            Low or negative correlations between indices indicate
            <b style="color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">diversification benefit</b> —
            combining them in a portfolio reduces overall volatility
            without proportionally reducing expected return.
            The heatmap uses a diverging colour scale:
          </div>
          <div style="margin-top:12px; line-height:2.0; font-size:0.82rem;">
            <span style="background:#004d00; padding:2px 10px; border-radius:4px; color:#fff;">Dark Green = +1.0 (perfect positive)</span><br>
            <span style="background:#2a3f5f; padding:2px 10px; border-radius:4px; color:#fff; margin-top:4px; display:inline-block;">Mid Blue = 0 (uncorrelated)</span><br>
            <span style="background:#8b0000; padding:2px 10px; border-radius:4px; color:#fff; margin-top:4px; display:inline-block;">Dark Red = −1.0 (perfect inverse)</span>
          </div>
        </div>""")

    # ── Section 6: Rankings Methodology ──
    st.html('''<div class="section-header">📐 Section 6 — Rankings & Composite Score</div>''')

    st.html(f"""
    <div class="metric-card" style="text-align:left; padding:18px 22px; margin-bottom:14px;">
      <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                  font-size:0.95rem; margin-bottom:12px;">How the Composite Score is Constructed</div>
      <div class="metric-sub" style="line-height:1.9;">
        Each index is ranked on <b>5 independent dimensions</b>. Rank 1 = best performer on that dimension.
        The Composite Score is the <b>simple arithmetic average</b> of the 5 individual ranks.
        The Overall Rank is then the ordinal position of the Composite Score (lowest = best).
      </div>
    </div>""")

    rank_rows = [
        ("Return Rank",    "Annualised Return",   "Descending (higher return = Rank 1)",     "Best risk-return tradeoff"),
        ("Volatility Rank","Ann. Volatility",     "Ascending  (lower vol = Rank 1)",         "Stability & capital preservation"),
        ("Sharpe Rank",    "Sharpe Ratio",        "Descending (higher Sharpe = Rank 1)",     "Risk-adjusted efficiency"),
        ("VaR Rank",       "95% VaR",             "Descending (least negative VaR = Rank 1)","Tail-risk protection"),
        ("Hit Rate Rank",  "Hit Rate (%)",        "Descending (higher hit rate = Rank 1)",   "Directional consistency"),
    ]

    for rank_name, metric, sort_logic, purpose in rank_rows:
        st.html(f"""
        <div class="metric-card" style="text-align:left; padding:14px 20px; margin-bottom:10px;
                                        border-left:4px solid {GOLD};">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                        font-size:0.9rem;">{rank_name}</div>
            <div style="background:rgba(255,215,0,0.12); border:1px solid rgba(255,215,0,0.3);
                        padding:2px 12px; border-radius:12px; font-size:0.75rem;
                        color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">{metric}</div>
          </div>
          <div class="metric-sub" style="margin-top:8px; font-size:0.82rem; line-height:1.7;">
            <b style="color:{TEXT_MAIN};-webkit-text-fill-color:{TEXT_MAIN};">Sort order:</b> {sort_logic}<br>
            <b style="color:{TEXT_MAIN};-webkit-text-fill-color:{TEXT_MAIN};">Purpose:</b> {purpose}
          </div>
        </div>""")

    st.html(f"""
    <div class="metric-card" style="text-align:left; padding:18px 22px; margin-top:6px;
                                    border:2px solid {GOLD};">
      <div style="color:{GOLD};-webkit-text-fill-color:{GOLD}; font-weight:700;
                  font-size:0.95rem; margin-bottom:10px;">⚠ Limitations & Caveats</div>
      <div class="metric-sub" style="line-height:1.9; font-size:0.85rem;">
        • <b>Equal weighting</b> of all 5 dimensions may not suit every investor's objective.<br>
        • Historical returns <b>do not guarantee future performance</b>.<br>
        • VaR and CVaR use <b>historical simulation</b> — extreme events not in the sample window are not captured.<br>
        • Annualisation via √12 assumes <b>i.i.d. returns</b> — autocorrelation (momentum/mean-reversion) is ignored.<br>
        • Correlations are <b>unconditional</b> — during crisis periods correlations typically spike toward +1.<br>
        • Data sourced from Yahoo Finance; <b>adjusted prices</b> account for dividends and splits but currency effects
          are not hedged across indices.<br>
        • Risk-free rate is fixed at 4.5% — users with different domiciles should adjust mentally.
      </div>
    </div>""")

    # ── Data sources ──
    st.html('''<div class="section-header">📡 Data Sources & Tickers</div>''')

    ticker_rows = [(name, meta["ticker"], meta["type"], meta["region"])
                   for name, meta in INDICES.items()]
    ticker_df = pd.DataFrame(ticker_rows, columns=["Index Name","Yahoo Ticker","Asset Type","Region"])
    st.dataframe(
        ticker_df.style
        .set_properties(**{"font-family":"JetBrains Mono,monospace",
                           "font-size":"11px","text-align":"left"})
        .set_table_styles([{"selector":"th",
                            "props":[("background-color",DARK_BLUE),("color",GOLD),
                                     ("font-weight","700"),("font-size","11px"),
                                     ("text-align","center")]}]),
        use_container_width=True, hide_index=True
    )

    st.html(f"""
    <div class="metric-card" style="text-align:center; padding:14px; margin-top:16px;">
      <div class="metric-sub" style="font-size:0.8rem; line-height:1.8;">
        Built with
        <b style="color:{LIGHT_BLUE};-webkit-text-fill-color:{LIGHT_BLUE};">Python 3 · Streamlit · yfinance · pandas · NumPy · Plotly</b><br>
        Data cached hourly via <code>@st.cache_data(ttl=3600)</code> ·
        For academic and educational use only.
      </div>
    </div>""")


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
