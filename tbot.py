import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- 1. CORE SYSTEM DEFINITIONS (CRITICAL ORDER) ---
# הגדרות אלו חייבות להופיע בראש הקוד ללא רווחים בתחילת השורה
BRAND_NAME = "SZ SOLUTIONS"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
israel_tz = pytz.timezone('Asia/Jerusalem')

# --- 2. SYSTEM CONFIGURATION ---
st.set_page_config(page_title=f"{BRAND_NAME} | SYSTEM", layout="wide")

# --- 3. PROFESSIONAL CENTERED UI (CSS) ---
st.markdown("""
    <style>
    /* Dark Industrial Theme */
    .stApp { background-color: #0A0C10; color: #AEB7C0; font-family: 'Inter', sans-serif; }
    
    /* Absolute Centering Logic for Mobile & Desktop */
    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
        margin: auto !important;
    }

    /* Modular Workstation Containers */
    .st-emotion-cache-12w0qpk { 
        background-color: #111418; 
        padding: 35px; 
        border-radius: 0px; 
        border: 1px solid #1F242C;
        margin-bottom: 25px;
        text-align: center !important;
    }
    
    /* Centering Headers & Metrics */
    h1, h2, h3, [data-testid="stMetric"], [data-testid="stMetricValue"] { 
        text-align: center !important;
        justify-content: center !important;
        width: 100%;
    }
    
    h1, h2, h3 { 
        color: #E6EDF3 !important; 
        text-transform: uppercase; 
        letter-spacing: 5px; 
        font-weight: 300 !important;
    }

    /* Precision Inputs */
    input { 
        background-color: #0D1117 !important; 
        border: 1px solid #30363D !important; 
        color: #C9D1D9 !important; 
        text-align: center !important;
        border-radius: 0px !important;
    }
    
    /* High-End Command Buttons */
    .stButton>button {
        width: 100%;
        max-width: 350px;
        border: 1px solid #30363D;
        background-color: #161B22;
        color: #8B949E;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 0px;
        margin: 10px auto !important;
        display: block;
    }
    .stButton>button:hover { border-color: #C9D1D9; color: #FFFFFF; }
    
    /* Execution Button Highlight */
    button[kind="primary"] { border: 1px solid #388BFD !important; color: #388BFD !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA PERSISTENCE ---
if 'history_log' not in st.session_state: st.session_state.history_log = []
if 'active_mode' not in st.session_state: st.session_state.active_mode = None

# --- HEADER SECTION ---
st.markdown(f"# {BRAND_NAME}")
current_ts = datetime.now(israel_tz).strftime('%H:%M:%S IST')
st.markdown(f"**STATUS: OPERATIONAL** // {current_ts}")
st.divider()

# --- MODULE 01: MARKET INTELLIGENCE ---
with st.container():
    st.markdown("### Market Intelligence")
    m1, m2, m3 = st.columns(3)
    try:
        val_sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        val_nas = yf.Ticker("^IXIC").history(period="1d")['Close'].iloc[-1]
        val_usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        m1.metric("S&P 500", f"{val_sp:,.2f}")
        m2.metric("NASDAQ", f"{val_nas:,.2f}")
        m3.metric("USD/ILS", f"{val_usd:.3f}")
    except: st.warning("LINK_SYNC_PENDING")

# --- MODULE 02: ANALYSIS ENGINE ---
with st.container():
    st.markdown("### Security Analysis")
    ticker_input = st.text_input("INPUT TICKER", value="NVDA").upper()
    
    c1, c2, c3 = st.columns(3)
    if c1.button("LOAD CHART"): st.session_state.active_mode = "chart"
    if c2.button("EXTRACT DATA"): st.session_state.active_mode = "intel"
    if c3.button("TERMINATE"): st.session_state.active_mode = None

    if st.session_state.active_mode == "chart":
        st.line_chart(yf.Ticker(ticker_input).history(period="1mo")['Close'])
    elif st.session_state.active_mode == "intel":
        st.write(yf.Ticker(ticker_input).info.get('longBusinessSummary', 'DATA_OFFLINE'))

# --- MODULE 03: RISK EXECUTION MATRIX ---
with st.container():
    st.markdown("### Risk Matrix")
    r1, r2, r3 = st.columns(3)
    val_ent = r1.number_input("ENTRY ($)", value=100.0)
    val_tp_p = r2.number_input("TP (%)", value=5.0)
    val_sl_p = r3.number_input("SL (%)", value=2.0)
    
    # המחשבון יופעל רק בלחיצה כאן
    if st.button("EXECUTE & LOG PARAMETERS", type="primary"):
        res_tp = val_ent * (1 + val_tp_p/100)
        res_sl = val_ent * (1 - val_sl_p/100)
        
        # רישום ללוג היומי
        st.session_state.history_log.insert(0, {
            "TIME": datetime.now(israel_tz).strftime("%H:%M"),
            "SYM": ticker_input,
            "ENT": f"{val_ent:.2f}",
            "TP": f"{res_tp:.2f}",
            "SL": f"{res_sl:.2f}",
            "RR": f"{val_tp_p/val_sl_p:.1f}"
        })
        
        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        res1.metric("TARGET", f"${res_tp:.2f}")
        res2.metric("STOP", f"${res_sl:.2f}")
        res3.metric("R/R", f"1:{val_tp_p/val_sl_p:.1f}")

# --- MODULE 04: SESSION HISTORY ---
if st.session_state.history_log:
    with st.container():
        st.markdown("### Session Log")
        st.table(pd.DataFrame(st.session_state.history_log))
        if st.button("CLEAR_LOG"):
            st.session_state.history_log = []
            st.rerun()

# --- FOOTER ---
st.divider()
st.caption(f"{BRAND_NAME} // SECURE_ID: {USER_KEY[:5]}***") [cite: 2025-12-22, 2025-12-23]
