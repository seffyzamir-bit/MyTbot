import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- CORE CONFIGURATION ---
BRAND_NAME = "SZ Solutions"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"  # Corrected Pushover Key [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | Terminal", layout="wide")

# --- PROFESSIONAL SILVER/STEEL THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #C9D1D9; }
    [data-testid="stMetricValue"] { color: #E0E0E0 !important; font-family: sans-serif; font-weight: bold; }
    .stButton>button {
        border: 1px solid #484F58;
        background-color: #21262D;
        color: #C9D1D9;
        border-radius: 4px;
    }
    .stButton>button:hover { border-color: #8B949E; color: #FFFFFF; }
    code { color: #A5D6FF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title(f"🔘 {BRAND_NAME} | Trading Terminal")
now = datetime.now(israel_tz)
st.code(f"SYSTEM: ACTIVE | {now.strftime('%Y-%m-%d %H:%M:%S')} IST", language="bash")

st.divider()

# --- MARKET PULSE ---
col_m1, col_m2 = st.columns(2)
try:
    m_sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
    m_usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
    col_m1.metric("S&P 500", f"{m_sp:,.2f}")
    col_m2.metric("USD/ILS", f"{m_usd:.3f}")
except Exception:
    st.warning("Fetching real-time data...")

st.divider()

# --- WATCHLIST (TARGET TRACKER) ---
st.subheader("🎯 Custom Price Scanner")
# Define your targets here
targets = {"NVDA": 900.0, "AAPL": 195.0, "MSFT": 430.0, "TSLA": 180.0}
wl_data = []
for sym, target in targets.items():
    try:
        curr = round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        wl_data.append({"Symbol": sym, "Target": target, "Live": curr, "Status": "READY" if curr >= target else "WATCH"})
    except: continue
st.table(pd.DataFrame(wl_data))

st.divider()

# --- ANALYSIS TOOLS ---
st.subheader("🔍 Analysis Tools")
symbol = st.text_input("Enter Ticker:", value="NVDA").upper()

if 'view' not in st.session_state: st.session_state.view = None

c1, c2, c3, c4 = st.columns(4)
if c1.button("📈 CHART"): st.session_state.view = "chart"
if c2.button("🌐 INTEL"): st.session_state.view = "intel"
if c3.button("📲 SYNC"): 
    st.toast(f"Pushing {symbol} to iPhone...") [cite: 2025-12-23]
if c4.button("❌ CLOSE"): st.session_state.view = None

if st.session_state.view == "chart":
    st.line_chart(yf.Ticker(symbol).history(period="1mo")['Close'])
elif st.session_state.view == "intel":
    st.info(f"Market Intel: {symbol}")
    st.write(yf.Ticker(symbol).info.get('longBusinessSummary', 'Searching...'))

st.divider()

# --- RISK CALCULATOR ---
st.subheader("🧮 SZ Risk Matrix")
cl1, cl2, cl3 = st.columns(3)
ent = cl1.number_input("Entry ($):", value=100.0)
t_p = cl2.number_input("TP (%):", value=5.0)
s_l = cl3.number_input("SL (%):", value=2.0)

tp_val = ent * (1 + t_p/100)
sl_val = ent * (1 - s_l/100)
st.code(f"CALC DATA | TP: ${tp_val:.2f} | SL: ${sl_val:.2f} | R/R: {t_p/s_l:.1f}", language="bash")

# --- FOOTER ---
st.markdown("---")
st.caption(f"© 2025 {BRAND_NAME} | Encrypted Link: {USER_KEY[:5]}***")
