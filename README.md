# 🌐 Global Index Monthly Return Tracker
### The Mountain Path – World of Finance
**Prof. V. Ravichandran** | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Run

```bash
streamlit run app.py
```

---

## 🌍 20 Global Indices Covered

### Equity Indices (14)
| Index | Region |
|-------|--------|
| S&P 500 (US) | Americas |
| NASDAQ 100 (US) | Americas |
| Dow Jones (US) | Americas |
| IBOVESPA (Brazil) | Americas |
| FTSE 100 (UK) | Europe |
| DAX 40 (Germany) | Europe |
| CAC 40 (France) | Europe |
| Nikkei 225 (Japan) | Asia-Pacific |
| Hang Seng (HK) | Asia-Pacific |
| CSI 300 (China) | Asia-Pacific |
| SENSEX (India) | Asia-Pacific |
| NIFTY 50 (India) | Asia-Pacific |
| ASX 200 (Australia) | Asia-Pacific |
| MSCI EM | Global |

### Commodity Indices (6)
| Index | Type |
|-------|------|
| Gold (XAU) | Precious Metal |
| Silver (XAG) | Precious Metal |
| WTI Crude Oil | Energy |
| Brent Crude | Energy |
| Natural Gas | Energy |
| Copper | Industrial Metal |

---

## 📊 Features

### Tab 1 – Monthly Heatmap
- Full colour-coded monthly return grid (green = gain, red = loss)
- Interactive Plotly heatmap with hover details
- Styled raw data table with conditional formatting
- CSV download button

### Tab 2 – Trend Charts
- Cumulative return chart (full period)
- Rolling 3-month return chart
- Latest month ranked horizontal bar chart

### Tab 3 – Annual Returns
- Grouped bar chart by year
- Annual return table with conditional colouring

### Tab 4 – Risk Statistics
- Average monthly & annualised return
- Monthly & annualised volatility
- Sharpe Ratio (assumed Rf = 4.5%)
- Max monthly gain / loss
- Skewness & Kurtosis
- Hit Rate (% positive months)
- VaR 95% & CVaR 95% (Historical Simulation)
- Risk-Return scatter plot
- Sharpe ratio bar chart
- CSV download

### Tab 5 – Correlation Matrix
- Full heatmap correlation matrix
- Highly correlated pairs table (|ρ| > 0.75)

---

## 🎨 Design
- Mountain Path palette: Dark Blue #003366 · Gold #FFD700 · Light Blue #ADD8E6
- Cinzel serif display font
- JetBrains Mono for numbers
- Responsive layout with animated hover cards

---

*Data sourced from Yahoo Finance via the `yfinance` library. For educational purposes only.*
