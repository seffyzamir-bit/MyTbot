import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# SZ Solutions Branding & Config
BRAND_NAME = "SZ Solutions"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | Trading OS", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to mimic the Desktop Bot looks
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #00FF41; /* Classic Matrix/Terminal Green */
    }
    /* Metric boxes */
    [data-testid="stMetricValue"] {
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Borders for sections */
    .stHeader, .stSubheader {
        border-bottom: 1px solid #30363d;
        padding-bottom: 10px;
    }
    /* Button styling */
    .stButton>button {
        border: 1px solid #00FF41;
        background-color: transparent;
        color: #00FF41;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button:hover {
        background-color: #00FF41;
        color: black;
    }
    /* Inputs */
    input {
        background-color: #161B22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"# ⚡ {BRAND_NAME} | Terminal Interface")
now = datetime.now(israel_tz)
st.code(f"SYSTEM STATUS: ONLINE | {now.strftime('%Y-%m-%d %H:%M:%S')} IST", language="bash")

st.divider()

# --- SECTION 1: MARKET PULSE (Indices) ---
col_m1, col_m2 = st.columns(2)
try:
    m_sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
    m_usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
    col_m1.metric("S&P 500 INDEX", f"{m_sp:,.2f}")
    col_m2.metric("USD/ILS EXCHANGE", f"{m_usd:.3f}")
except:
    st.error("Connection Error: Fetching Market Data...")

st.divider()

# --- SECTION 2: CUSTOM WATCHLIST ---
st.subheader("🎯 Active Watchlist")
targets = {"NVDA": 900.0, "AAPL": 195.0, "MSFT": 430.0, "TSLA": 180.0}
wl_list = []
for sym, target in targets.items():
    try:
        curr = round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        status = "HIT" if curr >= target else "WAIT"
        wl_list.append({"Ticker": sym, "Target": target, "Price": curr, "Status": status})
    except: continue

st.dataframe(pd.DataFrame(wl_list), use_container_width=True)

st.divider()

# --- SECTION 3: SCANNER & ANALYSIS ---
st.subheader("🔍 SZ Scanner Tool")
symbol = st.text_input("ENTER TICKER:", value="NVDA").upper()

if 'view' not in st.session_state: st.session_state.view = None

c1, c2, c3, c4 = st.columns(4)
if c1.button("📈 CHART"): st.session_state.view = "chart"
if c2.button("🌐 INTEL"): st.session_state.view = "intel"
if c3.button("📲 SYNC"): 
    st.session_state.view = "sync"
    st.toast("Alert synced to Pushover") [cite: 2025-12-22]
if c4.button("❌ CLOSE"): st.session_state.view = None

if st.session_state.view == "chart":
    st.line_chart(yf.Ticker(symbol).history(period="1mo")['Close'])
elif st.session_state.view == "intel":
    st.code(yf.Ticker(symbol).info.get('longBusinessSummary', 'No data found.'), language="text")

st.divider()

# --- SECTION 4: RISK CALCULATOR ---
st.subheader("🧮 SZ Risk Matrix")
with st.container():
    cl1, cl2, cl3 = st.columns(3)
    ent = cl1.number_input("ENTRY ($):", value=100.0)
    t_p = cl2.number_input("TP (%):", value=5.0)
    s_l = cl3.number_input("SL (%):", value=2.0)
    
    tp_val = ent * (1 + t_p/100)
    sl_val = ent * (1 - s_l/100)
    
    st.code(f"COMMAND: EXECUTE TRADE | TP: {tp_val:.2f} | SL: {sl_val:.2f} | R/R: {t_p/s_l:.1f}", language="bash")

st.caption(f"© 2025 SZ Solutions | Encrypted Link: {USER_KEY[:5]}***") [cite: 2025-12-22, 2025-12-23]
