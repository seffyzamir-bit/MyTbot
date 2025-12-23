import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- CORE CONFIGURATION ---
BRAND_NAME = "SZ SOLUTIONS"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | SYSTEM", layout="wide")

# --- ADVANCED CENTERED UI (CSS) ---
st.markdown("""
    <style>
    /* Base environment and Centering the main block */
    .stApp { 
        background-color: #0A0C10; 
        color: #AEB7C0; 
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Centering the container on the screen */
    .block-container {
        max-width: 900px !important;
        padding-top: 5rem !important;
        padding-bottom: 5rem !important;
        margin: auto !important;
    }

    /* Centering all module content */
    .st-emotion-cache-12w0qpk, .stMetric, .stMarkdown, h1, h2, h3 {
        text-align: center !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Modular Workstations */
    .st-emotion-cache-12w0qpk { 
        background-color: #111418; 
        padding: 40px; 
        border-radius: 2px; 
        border: 1px solid #1F242C;
        margin-bottom: 30px;
        width: 100%;
    }
    
    /* Professional Headers */
    h1, h2, h3 { 
        color: #E6EDF3 !important; 
        text-transform: uppercase; 
        letter-spacing: 4px; 
        font-weight: 300 !important;
        margin-bottom: 20px !important;
    }
    
    /* Precision Input Fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input { 
        background-color: #0D1117 !important; 
        border: 1px solid #30363D !important; 
        color: #C9D1D9 !important; 
        text-align: center !important;
        border-radius: 0px !important;
    }
    
    /* High-Tech Buttons */
    .stButton>button {
        width: 100%;
        max-width: 300px;
        border: 1px solid #30363D;
        background-color: #161B22;
        color: #8B949E;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 11px;
        border-radius: 0px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #21262D;
        border-color: #C9D1D9;
        color: #FFFFFF;
    }
    
    /* Primary Execution Button */
    button[kind="primary"] {
        border: 1px solid #388BFD !important;
        color: #388BFD !important;
    }

    /* Metric values centering */
    [data-testid="stMetricValue"] {
        width: 100%;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'history' not in st.session_state: st.session_state.history = []
if 'ui_view' not in st.session_state: st.session_state.ui_view = None

# --- HEADER SECTION ---
st.markdown(f"# {BRAND_NAME}")
now = datetime.now(israel_tz)
st.markdown(f"**SYSTEM STATUS: ACTIVE** // {now.strftime('%H:%M:%S IST')}")
st.divider()

# --- MODULE 01: GLOBAL INDICES ---
with st.container():
    st.markdown("### Market Intelligence")
    idx_1, idx_2, idx_3 = st.columns(3)
    try:
        sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        ns = yf.Ticker("^IXIC").history(period="1d")['Close'].iloc[-1]
        us = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        idx_1.metric("S&P 500", f"{sp:,.2f}")
        idx_2.metric("NASDAQ", f"{ns:,.2f}")
        idx_3.metric("USD / ILS", f"{us:.3f}")
    except: st.error("DATA_LINK_OFFLINE")

# --- MODULE 02: ANALYSIS ENGINE ---
with st.container():
    st.markdown("### Security Analysis")
    ticker = st.text_input("INPUT TICKER SYMBOL", value="NVDA").upper()
    
    a1, a2, a3 = st.columns(3)
    if a1.button("LOAD CHART"): st.session_state.ui_view = "chart"
    if a2.button("EXTRACT DATA"): st.session_state.ui_view = "intel"
    if a3.button("CLOSE"): st.session_state.ui_view = None

    if st.session_state.ui_view == "chart":
        st.line_chart(yf.Ticker(ticker).history(period="1mo")['Close'])
    elif st.session_state.ui_view == "intel":
        st.markdown(f"**ANALYSIS: {ticker}**")
        st.write(yf.Ticker(ticker).info.get('longBusinessSummary', 'N/A'))

# --- MODULE 03: EXECUTION CALCULATOR ---
with st.container():
    st.markdown("### Risk Matrix")
    ea, eb, ec = st.columns(3)
    f_ent = ea.number_input("ENTRY ($)", value=100.0)
    f_tp = eb.number_input("TP (%)", value=5.0)
    f_sl = ec.number_input("SL (%)", value=2.0)
    
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    if st.button("EXECUTE & LOG", type="primary"):
        v_tp = f_ent * (1 + f_tp/100)
        v_sl = f_ent * (1 - f_sl/100)
        
        st.session_state.history.insert(0, {
            "TIME": datetime.now(israel_tz).strftime("%H:%M"),
            "SYM": ticker,
            "ENT": f"{f_ent:.2f}",
            "TP": f"{v_tp:.2f}",
            "SL": f"{v_sl:.2f}",
            "RR": f"{f_tp/f_sl:.1f}"
        })
        
        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        res1.metric("TARGET", f"${v_tp:.2f}")
        res2.metric("STOP", f"${v_sl:.2f}")
        res3.metric("R/R", f"1:{f_tp/f_sl:.1f}")
        st.toast("LOG_SUCCESS") [cite: 2025-12-23]

# --- MODULE 04: SESSION LOG ---
if st.session_state.history:
    with st.container():
        st.markdown("### Session Log")
        st.table(pd.DataFrame(st.session_state.history))
        if st.button("RESET LOG"):
            st.session_state.history = []
            st.rerun()

# --- FOOTER ---
st.divider()
st.caption(f"{BRAND_NAME} // SECURE_ID: {USER_KEY[:5]}***") [cite: 2025-12-22, 2025-12-23]
