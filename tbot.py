import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- 1. GLOBAL CORE VARIABLES ---
# Critical: These must be defined first at the top level
BRAND_NAME = "SZ SOLUTIONS"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | SYSTEM", layout="wide")

# --- 2. ADVANCED CENTERED WORKSTATION UI (CSS) ---
st.markdown("""
    <style>
    /* Dark Slate Environment */
    .stApp { background-color: #0A0C10; color: #AEB7C0; font-family: 'Inter', sans-serif; }
    
    /* Absolute Centering Logic */
    .block-container {
        max-width: 800px !important;
        padding-top: 3rem !important;
        margin: auto !important;
    }

    /* Professional Modules */
    .st-emotion-cache-12w0qpk { 
        background-color: #111418; 
        padding: 40px; 
        border-radius: 0px; 
        border: 1px solid #1F242C;
        margin-bottom: 25px;
        text-align: center !important;
    }
    
    /* Monochrome Typography */
    h1, h2, h3 { 
        color: #E6EDF3 !important; 
        text-transform: uppercase; 
        letter-spacing: 5px; 
        font-weight: 300 !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    
    /* Metrics alignment */
    [data-testid="stMetric"] { text-align: center !important; }
    [data-testid="stMetricValue"] { font-size: 26px !important; color: #FFFFFF !important; }

    /* Industrial Inputs */
    input { 
        background-color: #0D1117 !important; 
        border: 1px solid #30363D !important; 
        color: #C9D1D9 !important; 
        text-align: center !important;
        border-radius: 0px !important;
    }
    
    /* Command Buttons */
    .stButton>button {
        width: 100%;
        border: 1px solid #30363D;
        background-color: #161B22;
        color: #8B949E;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 0px;
        font-size: 11px;
    }
    .stButton>button:hover { border-color: #C9D1D9; color: #FFFFFF; }
    
    /* Execution Primary */
    button[kind="primary"] { border: 1px solid #388BFD !important; color: #388BFD !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT STATE ---
if 'log_data' not in st.session_state: st.session_state.log_data = []
if 'view_mode' not in st.session_state: st.session_state.view_mode = None

# --- TOP INTERFACE ---
st.markdown(f"# {BRAND_NAME}")
curr_time = datetime.now(israel_tz).strftime('%H:%M:%S IST')
st.markdown(f"**INTERFACE STATUS: OPERATIONAL** // {curr_time}")
st.divider()

# --- MODULE 01: MARKET INTELLIGENCE ---
with st.container():
    st.markdown("### Market Intelligence")
    m_col1, m_col2, m_col3 = st.columns(3)
    try:
        data_sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        data_nas = yf.Ticker("^IXIC").history(period="1d")['Close'].iloc[-1]
        data_usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        m_col1.metric("S&P 500", f"{data_sp:,.2f}")
        m_col2.metric("NASDAQ", f"{data_nas:,.2f}")
        m_col3.metric("USD/ILS", f"{data_usd:.3f}")
    except: st.warning("LINK_SYNC_PENDING")

# --- MODULE 02: ASSET ANALYSIS ---
with st.container():
    st.markdown("### Security Analysis")
    target_sym = st.text_input("INPUT TICKER", value="NVDA").upper()
    
    b_col1, b_col2, b_col3 = st.columns(3)
    if b_col1.button("LOAD CHART"): st.session_state.view_mode = "chart"
    if b_col2.button("EXTRACT DATA"): st.session_state.view_mode = "intel"
    if b_col3.button("TERMINATE"): st.session_state.view_mode = None

    if st.session_state.view_mode == "chart":
        st.line_chart(yf.Ticker(target_sym).history(period="1mo")['Close'])
    elif st.session_state.view_mode == "intel":
        st.write(yf.Ticker(target_sym).info.get('longBusinessSummary', 'DATA_NOT_FOUND'))

# --- MODULE 03: RISK MATRIX ---
with st.container():
    st.markdown("### Risk Execution Matrix")
    r_col1, r_col2, r_col3 = st.columns(3)
    p_ent = r_col1.number_input("ENTRY_VAL", value=100.0)
    p_tp = r_col2.number_input("TP_PERCENT", value=5.0)
    p_sl = r_col3.number_input("SL_PERCENT", value=2.0)
    
    if st.button("EXECUTE & LOG PARAMETERS", type="primary"):
        calc_tp = p_ent * (1 + p_tp/100)
        calc_sl = p_ent * (1 - p_sl/100)
        
        # Internal Recording
        st.session_state.log_data.insert(0, {
            "TIMESTAMP": datetime.now(israel_tz).strftime("%H:%M"),
            "TICKER": target_sym,
            "ENTRY": f"{p_ent:.2f}",
            "TP_TARGET": f"{calc_tp:.2f}",
            "SL_LIMIT": f"{calc_sl:.2f}"
        })
        
        st.markdown("---")
        res_c1, res_c2, res_c3 = st.columns(3)
        res_c1.metric("TARGET", f"${calc_tp:.2f}")
        res_c2.metric("STOP", f"${calc_sl:.2f}")
        res_c3.metric("R/R", f"1:{p_tp/p_sl:.1f}")

# --- MODULE 04: SESSION LOG ---
if st.session_state.log_data:
    with st.container():
        st.markdown("### Session Log")
        st.table(pd.DataFrame(st.session_state.log_data))
        if st.button("CLEAR_SESSION_LOG"):
            st.session_state.log_data = []
            st.rerun()

# --- FOOTER ---
st.divider()
st.caption(f"{BRAND_NAME} // SYSTEM_ID: {USER_KEY[:5]}***") [cite: 2025-12-22, 2025-12-23]
