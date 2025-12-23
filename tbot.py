import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- 1. CORE SYSTEM CONFIGURATION ---
# מוגדר בראש הקוד כדי למנוע NameError
BRAND_NAME = "SZ SOLUTIONS"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" 
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | SYSTEM", layout="wide")

# --- 2. FUTURISTIC CENTERED UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0C10; color: #AEB7C0; font-family: 'Inter', sans-serif; }
    
    /* Centering the main workspace */
    .block-container {
        max-width: 800px !important;
        padding-top: 4rem !important;
        margin: auto !important;
    }

    /* Module Containers */
    .st-emotion-cache-12w0qpk { 
        background-color: #111418; 
        padding: 40px; 
        border-radius: 0px; 
        border: 1px solid #1F242C;
        margin-bottom: 25px;
        text-align: center !important;
    }
    
    /* Clean Typography */
    h1, h2, h3 { 
        color: #E6EDF3 !important; 
        text-transform: uppercase; 
        letter-spacing: 5px; 
        font-weight: 300 !important;
        text-align: center !important;
        width: 100%;
    }
    
    /* Centered Metrics */
    [data-testid="stMetric"] { text-align: center !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; color: #FFFFFF !important; }

    /* Inputs & Buttons */
    input { 
        background-color: #0D1117 !important; 
        border: 1px solid #30363D !important; 
        color: #C9D1D9 !important; 
        text-align: center !important;
        border-radius: 0px !important;
    }
    
    .stButton>button {
        width: 100%;
        border: 1px solid #30363D;
        background-color: #161B22;
        color: #8B949E;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 0px;
        transition: 0.4s;
    }
    .stButton>button:hover { border-color: #C9D1D9; color: #FFFFFF; }
    
    button[kind="primary"] { border: 1px solid #388BFD !important; color: #388BFD !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION MANAGEMENT ---
if 'log' not in st.session_state: st.session_state.log = []
if 'view' not in st.session_state: st.session_state.view = None

# --- HEADER ---
st.markdown(f"# {BRAND_NAME}")
now = datetime.now(israel_tz)
st.markdown(f"**CORE_SYSTEM_ACTIVE** // {now.strftime('%H:%M:%S IST')}")
st.divider()

# --- MODULE 01: GLOBAL MARKET ---
with st.container():
    st.markdown("### Market Intelligence")
    m1, m2, m3 = st.columns(3)
    try:
        sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        ns = yf.Ticker("^IXIC").history(period="1d")['Close'].iloc[-1]
        usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        m1.metric("S&P 500", f"{sp:,.2f}")
        m2.metric("NASDAQ", f"{ns:,.2f}")
        m3.metric("USD/ILS", f"{usd:.3f}")
    except: st.error("LINK_FAILURE")

# --- MODULE 02: ANALYSIS ENGINE ---
with st.container():
    st.markdown("### Security Analysis")
    ticker = st.text_input("TICKER_SYMBOL", value="NVDA").upper()
    
    c1, c2, c3 = st.columns(3)
    if c1.button("LOAD CHART"): st.session_state.view = "chart"
    if c2.button("EXTRACT DATA"): st.session_state.view = "intel"
    if c3.button("CLOSE"): st.session_state.view = None

    if st.session_state.view == "chart":
        st.line_chart(yf.Ticker(ticker).history(period="1mo")['Close'])
    elif st.session_state.view == "intel":
        st.write(yf.Ticker(ticker).info.get('longBusinessSummary', 'N/A'))

# --- MODULE 03: RISK MATRIX ---
with st.container():
    st.markdown("### Execution Matrix")
    ea, eb, ec = st.columns(3)
    f_ent = ea.number_input("ENTRY ($)", value=100.0)
    f_tp = eb.number_input("TP (%)", value=5.0)
    f_sl = ec.number_input("SL (%)", value=2.0)
    
    if st.button("EXECUTE & LOG PARAMETERS", type="primary"):
        v_tp = f_ent * (1 + f_tp/100)
        v_sl = f_ent * (1 - f_sl/100)
        
        st.session_state.log.insert(0, {
            "TIME": datetime.now(israel_tz).strftime("%H:%M"),
            "SYM": ticker,
            "ENT": f"{f_ent:.2f}",
            "TP": f"{v_tp:.2f}",
            "SL": f"{v_sl:.2f}"
        })
        
        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        res1.metric("TARGET", f"${v_tp:.2f}")
        res2.metric("STOP", f"${v_sl:.2f}")
        res3.metric("R/R", f"1:{f_tp/f_sl:.1f}")

# --- MODULE 04: SESSION LOG ---
if st.session_state.log:
    with st.container():
        st.markdown("### Session Log")
        st.table(pd.DataFrame(st.session_state.log))
        if st.button("RESET LOG"):
            st.session_state.log = []
            st.rerun()

# --- FOOTER ---
st.divider()
st.caption(f"{BRAND_NAME} // SECURE_ID: {USER_KEY[:5]}***")
