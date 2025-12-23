import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- CORE CONFIGURATION ---
BRAND_NAME = "SZ Solutions"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | OS", layout="wide")

# --- HIGH-END STEEL THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #D1D5DB; }
    
    /* Modular Card Styling */
    .st-emotion-cache-12w0qpk { 
        background-color: #161B22; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #30363D;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    h1, h2, h3 { color: #F0F6FC !important; font-family: 'Inter', sans-serif; letter-spacing: -0.5px; }
    
    /* Professional Silver Buttons */
    .stButton>button {
        width: 100%;
        border: 1px solid #484F58;
        background-color: #21262D;
        color: #C9D1D9;
        font-weight: 600;
        padding: 10px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #30363D;
        border-color: #8B949E;
        color: #FFFFFF;
    }
    
    /* Table Styling */
    .stDataFrame { border: 1px solid #30363D; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'view' not in st.session_state:
    st.session_state.view = None

# --- HEADER ---
col_logo, col_status = st.columns([3, 1])
with col_logo:
    st.title(f"🔘 {BRAND_NAME} OS")
with col_status:
    now = datetime.now(israel_tz)
    st.write(f"**CORE: ACTIVE**")
    st.caption(now.strftime('%H:%M:%S IST'))

st.divider()

# --- MODULE 1: MARKET INTELLIGENCE ---
with st.container():
    st.subheader("📊 Market Intelligence")
    m1, m2, m3 = st.columns(3)
    try:
        sp = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        nas = yf.Ticker("^IXIC").history(period="1d")['Close'].iloc[-1]
        m1.metric("S&P 500", f"{sp:,.2f}")
        m2.metric("NASDAQ", f"{nas:,.2f}")
        m3.metric("USD/ILS", f"{usd:.3f}")
    except: st.error("Market Data Link Failed")

# --- MODULE 2: SECURITY ANALYSIS ---
with st.container():
    st.subheader("🔍 Security Analysis")
    symbol = st.text_input("ENTER TICKER:", value="NVDA").upper()
    
    c1, c2, c3 = st.columns(3)
    if c1.button("📈 GENERATE CHART"): st.session_state.view = "chart"
    if c2.button("🌐 FETCH INTEL"): st.session_state.view = "intel"
    if c3.button("❌ CLOSE VIEW"): st.session_state.view = None

    if st.session_state.view == "chart":
        st.line_chart(yf.Ticker(symbol).history(period="1mo")['Close'])
    elif st.session_state.view == "intel":
        st.info(f"SZ Intelligence Report: {symbol}")
        st.write(yf.Ticker(symbol).info.get('longBusinessSummary', 'No data available.'))

# --- MODULE 3: TRADE EXECUTION CALCULATOR ---
with st.container():
    st.subheader("🧮 Execution Matrix")
    ca, cb, cc = st.columns(3)
    ent = ca.number_input("Entry Price ($):", value=100.0)
    tp_p = cb.number_input("Target Profit (%):", value=5.0)
    sl_p = cc.number_input("Stop Loss (%):", value=2.0)
    
    if st.button("🚀 EXECUTE & LOG", type="primary"):
        tp_v = ent * (1 + tp_p/100)
        sl_v = ent * (1 - sl_p/100)
        rr = tp_p / sl_p
        
        # Save to History
        trade_entry = {
            "Time": datetime.now(israel_tz).strftime("%H:%M"),
            "Symbol": symbol,
            "Entry": f"${ent:.2f}",
            "TP": f"${tp_v:.2f}",
            "SL": f"${sl_v:.2f}",
            "R/R": f"1:{rr:.1f}"
        }
        st.session_state.trade_history.insert(0, trade_entry)
        
        # Display Results
        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        res1.metric("EXIT TARGET", f"${tp_v:.2f}")
        res2.metric("STOP LIMIT", f"${sl_v:.2f}")
        res3.metric("R/R RATIO", f"1:{rr:.1f}")
        st.toast("Trade logged and synced.") [cite: 2025-12-23]

# --- MODULE 4: TRADE HISTORY ---
if st.session_state.trade_history:
    with st.container():
        st.subheader("📜 Daily Trade Log")
        history_df = pd.DataFrame(st.session_state.trade_history)
        st.table(history_df)
        if st.button("🗑️ Clear History"):
            st.session_state.trade_history = []
            st.rerun()

# --- FOOTER ---
st.divider()
st.caption(f"© 2025 {BRAND_NAME} | Terminal Encrypted | ID: {USER_KEY[:5]}***") [cite: 2025-12-22]
