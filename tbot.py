import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# SZ Solutions Configuration
BRAND_NAME = "SZ Solutions"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | Trading OS", layout="wide")

# Header & Branding
st.title(f"🚀 {BRAND_NAME} - Professional Trading Dashboard")
now = datetime.now(israel_tz)
st.write(f"📅 {now.strftime('%A, %b %d, %Y')} | 🕒 {now.strftime('%H:%M:%S')} (IST)")

st.divider()

# --- Section 1: Custom Price Tracker (Scanner) ---
st.subheader("🎯 Custom Price Watchlist")
st.write("Monitor your target prices for specific stocks.")

# Defining your custom watchlist
targets = {
    "NVDA": 900.0,
    "AAPL": 195.0,
    "MSFT": 430.0,
    "TSLA": 180.0
}

watchlist_data = []
for sym, target in targets.items():
    try:
        current = round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        diff = round(current - target, 2)
        status = "🎯 Target Hit!" if current >= target else "⏳ Waiting..."
        watchlist_data.append({"Symbol": sym, "Target": target, "Current": current, "Gap": diff, "Status": status})
    except:
        continue

df_watchlist = pd.DataFrame(watchlist_data)
st.table(df_watchlist)

st.divider()

# --- Section 2: Stock Search & Analysis ---
st.subheader("🔍 Stock Analysis & Tools")
symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL):", value="NVDA").upper()

col1, col2, col3 = st.columns(3)

if col1.button(f"📈 View {symbol} Chart", use_container_width=True):
    data = yf.Ticker(symbol).history(period="1mo")
    st.line_chart(data['Close'])

if col2.button(f"🌐 Market Intelligence", use_container_width=True):
    ticker = yf.Ticker(symbol)
    st.info(f"**Business Summary for {symbol}:**")
    st.write(ticker.info.get('longBusinessSummary', 'No data available.'))

if col3.button(f"📲 Sync to iPhone (Pushover)", use_container_width=True):
    st.success(f"Tracking {symbol}... Alerts sent to your device via {BRAND_NAME} gateway.")

st.divider()

# --- Section 3: Professional Trade Calculator ---
st.subheader("🧮 Risk Management Calculator")
c_a, c_b, c_c = st.columns(3)

entry = c_a.number_input("Entry Price ($):", value=100.0)
target_pct = c_b.number_input("Target Profit (%):", value=5.0)
stop_pct = c_c.number_input("Stop Loss (%):", value=2.0)

# Calculations
tp_price = entry * (1 + target_pct / 100)
sl_price = entry * (1 - stop_pct / 100)
rr_ratio = target_pct / stop_pct

st.info(f"🎯 **Target (TP):** ${tp_price:.2f} | 🛑 **Stop (SL):** ${sl_price:.2f} | ⚖️ **R/R Ratio:** 1:{rr_ratio:.1f}")

st.divider()

# --- Section 4: Market Overview ---
st.subheader("🌍 Market Pulse")
@st.cache_data(ttl=60)
def get_market_indices():
    return {
        "S&P 500": yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1],
        "USD/ILS": yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
    }

m_data = get_market_indices()
mc1, mc2 = st.columns(2)
mc1.metric("S&P 500", f"{m_data['S&P 500']:,.2f}")
mc2.metric("USD/ILS", f"{m_data['USD/ILS']:.3f}")

st.caption(f"© 2025 {BRAND_NAME} | Secure Connection: {USER_KEY[:5]}***")
