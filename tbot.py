import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- SZ SOLUTIONS CORE CONFIG ---
BRAND_NAME = "SZ Solutions"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" # [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | OS", layout="wide")

# --- INDUSTRIAL PRO THEME (SILVER & SLATE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0D1117; color: #C9D1D9; }
    
    /* Workstation Module Styling */
    .st-emotion-cache-12w0qpk { 
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #30363D;
        margin-bottom: 20px;
    }
    
    h1, h2, h3 { color: #F0F6FC !important; font-family: 'Inter', sans-serif; }
    
    /* Professional Steel Buttons */
    .stButton>button {
        width: 100%;
        border: 1px solid #484F58;
        background-color: #21262D;
        color: #C9D1D9;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #30363D;
        border-color: #8B949E;
        color: #FFFFFF;
    }
    
    /* Metrics and Data */
    [data-testid="stMetricValue"] { color: #F0F6FC !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STORAGE ---
if 'trade_log' not in st.session_state:
    st.session_state.trade_log = []
if 'active_view' not in st.session_state:
    st.session_state.active_view = None

# --- HEADER ---
c_logo, c_time = st.columns([3, 1])
with c_logo:
    st.title(f"🔘 {BRAND_NAME} Operating System")
with c_time:
    t_now = datetime.now(israel_tz)
    st.write(f"**SYSTEM ONLINE**")
    st.caption(t_now.strftime('%H:%M:%S IST'))

st.divider()

# --- MODULE 1: GLOBAL MARKET PULSE ---
with st.container():
    st.subheader("📊 Market Intelligence")
    m1, m2, m3 = st.columns(3)
    try:
        sp_val = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        usd_val = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        nas_val = yf.Ticker("^IXIC").history(period="1d")['Close'].iloc[-1]
        m1.metric("S&P 500", f"{sp_val:,.2f}")
        m2.metric("NASDAQ", f"{nas_val:,.2f}")
        m3.metric("USD/ILS", f"{usd_val:.3f}")
    except: st.warning("Data sync in progress...")

# --- MODULE 2: SECURITY SCANNER & ANALYSIS ---
with st.container():
    st.subheader("🔍 Security Analysis")
    sym = st.text_input("ENTER TICKER SYMBOL:", value="NVDA").upper()
    
    b1, b2, b3 = st.columns(3)
    if b1.button("📈 GENERATE CHART"): st.session_state.active_view = "chart"
    if b2.button("🌐 FETCH INTEL"): st.session_state.active_view = "intel"
    if b3.button("❌ CLOSE WINDOW"): st.session_state.active_view = None

    if st.session_state.active_view == "chart":
        st.line_chart(yf.Ticker(sym).history(period="1mo")['Close'])
    elif st.session_state.active_view == "intel":
        st.info(f"SZ Analysis Report: {sym}")
        st.write(yf.Ticker(sym).info.get('longBusinessSummary', 'No data available.'))

# --- MODULE 3: TRADE CALCULATOR & LOGGER ---
with st.container():
    st.subheader("🧮 Trade Execution Matrix")
    c_ent, c_tp, c_sl = st.columns(3)
    val_ent = c_ent.number_input("Entry Price ($):", value=100.0)
    val_tp_p = c_tp.number_input("Target Profit (%):", value=5.0)
    val_sl_p = c_sl.number_input("Stop Loss (%):", value=2.0)
    
    # MANUAL CALCULATION TRIGGER
    if st.button("🚀 EXECUTE & LOG TRADE", type="primary"):
        res_tp = val_ent * (1 + val_tp_p/100)
        res_sl = val_ent * (1 - val_sl_p/100)
        res_rr = val_tp_p / val_sl_p
        
        # Save to Daily Log
        log_entry = {
            "Time": datetime.now(israel_tz).strftime("%H:%M"),
            "Symbol": sym,
            "Entry": f"${val_ent:.2f}",
            "TP Target": f"${res_tp:.2f}",
            "SL Limit": f"${res_sl:.2f}",
            "R/R": f"1:{res_rr:.1f}"
        }
        st.session_state.trade_log.insert(0, log_entry)
        
        # Display Results
        st.markdown("---")
        r1, r2, r3 = st.columns(3)
        r1.metric("EXIT TARGET", f"${res_tp:.2f}")
        r2.metric("STOP LIMIT", f"${res_sl:.2f}")
        r3.metric("R/R RATIO", f"1:{res_rr:.1f}")
        st.toast("Trade recorded in Daily Log.") [cite: 2025-12-23]

# --- MODULE 4: DAILY TRADE LOG ---
if st.session_state.trade_log:
    with st.container():
        st.subheader("📜 Daily Trade History")
        st.table(pd.DataFrame(st.session_state.trade_log))
        if st.button("🗑️ Reset Daily Log"):
            st.session_state.trade_log = []
            st.rerun()

# --- FOOTER ---
st.divider()
st.caption(f"© 2025 {BRAND_NAME} | Secure Terminal | Link: {USER_KEY[:5]}***") [cite: 2025-12-22]
