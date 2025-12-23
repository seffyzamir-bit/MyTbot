import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# SZ Solutions Configuration [cite: 2025-12-23]
BRAND_NAME = "SZ Solutions"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | Terminal", layout="wide")

# Professional Silver/Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stApp { background-color: #0E1117; color: #C0C0C0; } /* Silver Text */
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { color: #E0E0E0 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #8B949E !important; }

    /* Button Styling - Silver/Steel */
    .stButton>button {
        border: 1px solid #484F58;
        background-color: #21262D;
        color: #C9D1D9;
        border-radius: 4px;
        font-weight: 500;
    }
    .stButton>button:hover {
        border-color: #8B949E;
        color: #FFFFFF;
        background-color: #30363D;
    }

    /* Input boxes */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #0D1117 !important;
        color: #C9D1D9 !important;
        border: 1px solid #30363d !important;
    }

    /* Terminal-style code blocks */
    code { color: #A5D6FF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & STATUS ---
st.title(f"🔘 {BRAND_NAME} | Trading Terminal")
now = datetime.now(israel_tz)
st.code(f"STATUS: SYSTEM_ACTIVE | {now.strftime('%Y-%m-%d %H:%M:%S')} IST", language="bash")

st.divider()

# --- MARKET PULSE ---
col_m1, col_m2 = st.columns(2)
try:
    m_sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
    m_usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
    col_m1.metric("S&P 500", f"{m_sp:,.2f}")
    col_m2.metric("USD/ILS", f"{m_usd:.3f}")
except:
    st.warning("Reconnecting to market data...")

st.divider()

# --- WATCHLIST ---
st.subheader("📋 Price Monitoring")
targets = {"NVDA": 900.0, "AAPL": 195.0, "MSFT": 430.0, "TSLA": 180.0}
wl_list = []
for sym, target in targets.items():
    try:
        curr = round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        wl_list.append({"Symbol": sym, "Target": target, "Live": curr, "Status": "Target Area" if curr >= target else "Tracking"})
    except: continue
st.dataframe(pd.DataFrame(wl_list), use_container_width=True)

st.divider()

# --- TOOLS & ANALYSIS ---
st.subheader("🔍 Analysis Tools")
symbol = st.text_input("ENTER TICKER:", value="NVDA").upper()

if 'view' not in st.session_state: st.session_state.view = None

c1, c2, c3, c4 = st.columns(4)
if c1.button("📈 CHART"): st.session_state.view = "chart"
if c2.button("🌐 INTEL"): st.session_state.view = "intel"
if c3.button("📲 SYNC"): 
    st.session_state.view = "sync"
    st.toast(f"Syncing {symbol} to Pushover...") [cite: 2025-12-23]
if c4.button("❌ CLOSE"): st.session_state.view = None

if st.session_state.view == "chart":
    st.line_chart(yf.Ticker(symbol).history(period="1mo")['Close'])
elif st.session_state.view == "intel":
    st.info(f"Market Analysis for {symbol}")
    st.write(yf.Ticker(symbol).info.get('longBusinessSummary', 'No data available.'))

st.divider()

# --- RISK CALCULATOR (FIXED) ---
st.subheader("🧮 Calculator")
with st.container():
    cl1, cl2, cl3 = st.columns(3)
    ent = cl1.number_input("Entry ($):", value=100.0)
    t_p = cl2.number_input("TP (%):", value=5.0)
    s_l = cl3.number_input("SL (%):", value=2.0)
    
    tp_val = ent * (1 + t_p/100)
    sl_val = ent * (1 - s_l/100)
    
    st.code(f"EXECUTION DATA | TP: ${tp_val:.2f} | SL: ${sl_val:.2f} | R/R: {t_p/s_l:.1f}", language="bash")

# --- FOOTER (FIXED Error) ---
st.markdown("---")
st.caption(f"© 2025 {BRAND_NAME} | Encrypted Link: {USER_KEY[:5]}***")
