import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- 1. CORE DEFINITIONS (CRITICAL: MUST BE TOP-LEVEL) ---
# הגדרות ליבה בראש הקוד למניעת NameError
BRAND_NAME = "SZ SOLUTIONS"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | OS", layout="wide")

# --- 2. MATTE BLACK & SILVER DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Main Environment */
    .stApp { background-color: #050505; color: #C0C0C0; font-family: 'Inter', sans-serif; }
    
    /* Center Layout */
    .block-container { max-width: 800px !important; padding-top: 1.5rem !important; margin: auto !important; }
    
    /* Professional Modules */
    .st-emotion-cache-12w0qpk { 
        background-color: #0F0F0F; padding: 20px; border-radius: 2px; 
        border: 1px solid #1A1A1A; margin-bottom: 20px; text-align: center !important;
    }
    
    /* Branding & Titles */
    h1 { color: #FFFFFF !important; letter-spacing: 10px; font-weight: 200 !important; text-align: center !important; margin-bottom: 5px !important; }
    h3 { color: #808080 !important; text-transform: uppercase; letter-spacing: 3px; font-size: 13px !important; text-align: center !important; margin-bottom: 15px !important; }
    
    /* Precision Inputs (Matte Black Style) */
    input { 
        background-color: #0A0A0A !important; border: 1px solid #262626 !important; 
        color: #FFFFFF !important; text-align: center !important; border-radius: 0px !important;
    }
    
    /* Control Buttons (Silver/Grey) */
    .stButton>button {
        border: 1px solid #262626; background-color: #0F0F0F; color: #8B949E;
        letter-spacing: 1px; text-transform: uppercase; border-radius: 0px; font-size: 10px;
        transition: 0.3s; width: auto !important; min-width: 80px; padding: 5px 15px !important;
    }
    .stButton>button:hover { border-color: #C0C0C0; color: #FFFFFF; background-color: #1A1A1A; }
    
    /* Matrix Execution (Deep Green) */
    button[kind="primary"] { 
        border: 1px solid #004D00 !important; color: #00FF00 !important; 
        background-color: #051405 !important; font-weight: bold !important;
        width: 100% !important; max-width: 400px !important; margin: 20px auto !important; display: block !important;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] { font-size: 24px !important; color: #FFFFFF !important; }
    [data-testid="stMetricLabel"] { font-size: 11px !important; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT STATE ---
if 'matrix_active' not in st.session_state: st.session_state.matrix_active = False
if 'active_view' not in st.session_state: st.session_state.active_view = None

# --- HEADER: SZ SOLUTIONS ---
st.markdown(f"<h1>{BRAND_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#404040; font-size:10px; letter-spacing:2px;'>SYSTEM STATUS: OPERATIONAL // {datetime.now(israel_tz).strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
st.divider()

# --- MODULE 01: MARKET INTELLIGENCE (INDEX TABLE) ---
with st.container():
    st.markdown("### Market Intelligence")
    idx_map = {
        "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "RSP (EQUAL)": "RSP", 
        "RUSSELL 2000": "^RUT", "BITCOIN": "BTC-USD", "USD/ILS": "USDILS=X"
    }
    
    # פריסה של 3 עמודות לטובת מובייל
    m_cols = st.columns(3)
    for idx, (label, ticker) in enumerate(idx_map.items()):
        with m_cols[idx % 3]:
            try:
                val = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
                st.metric(label, f"{val:,.2f}" if "USD" not in ticker else f"{val:.3f}")
                # כפתור קישור ישיר לגוגל פייננס
                clean_ticker = ticker.replace('^', '')
                st.markdown(f"<div style='text-align:center;'><a href='https://www.google.com/finance/quote/{clean_ticker}' style='color:#404040; font-size:9px; text-decoration:none;'>[G_FINANCE]</a></div>", unsafe_allow_html=True)
            except: st.caption("SYNC...")

# --- MODULE 02: SECURITY ANALYSIS (TRACKER) ---
with st.container():
    st.markdown("### Security Analysis")
    # שורת טיקר ארוכה כפי שביקשת
    target_ticker = st.text_input("INPUT TICKER SYMBOL", placeholder="E.G. NVDA", label_visibility="collapsed").upper()
    
    # כפתורי בקרה קטנים וממורכזים תחתיה
    b_col1, b_col2, b_col3 = st.columns([1, 1, 0.5])
    if b_col1.button("LOAD CHART"): st.session_state.active_view = "chart"
    if b_col2.button("EXTRACT DATA"): st.session_state.active_view = "intel"
    if b_col3.button("X"): st.session_state.active_view = None

    if st.session_state.active_view == "chart" and target_ticker:
        st.line_chart(yf.Ticker(target_ticker).history(period="1mo")['Close'])
    elif st.session_state.active_view == "intel" and target_ticker:
        st.write(yf.Ticker(target_ticker).info.get('longBusinessSummary', 'DATA_OFFLINE'))

# --- MODULE 03: RISK MATRIX (CENTERED CALCULATOR) ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("OPEN RISK MATRIX", type="primary"):
    st.session_state.matrix_active = not st.session_state.matrix_active

if st.session_state.matrix_active:
    with st.container():
        st.markdown("### Risk Matrix")
        r_col1, r_col2, r_col3 = st.columns(3)
        # שימוש ב-Placeholder כפי שביקשת (מוטבע בתוך השורה)
        f_entry = r_col1.text_input("ENTRY_PRC", placeholder="ENTRY $")
        f_tp_pct = r_col2.text_input("TP_TARGET", placeholder="TP %")
        f_sl_pct = r_col3.text_input("SL_LIMIT", placeholder="SL %")
        
        if f_entry and f_tp_pct and f_sl_pct:
            try:
                e_val, tp_val, sl_val = float(f_entry), float(f_tp_pct), float(f_sl_pct)
                t_price = e_val * (1 + tp_val/100)
                s_price = e_val * (1 - sl_val/100)
                
                # תוצאות מעוצבות
                st.markdown(f"""
                <div style='background-color:#051405; border:1px solid #004D00; padding:15px; text-align:center;'>
                    <span style='color:#00FF00; font-size:12px; letter-spacing:1px;'>TARGET: ${t_price:.2f} | STOP: ${s_price:.2f} | R/R: {tp_val/sl_val:.1f}</span>
                </div>
                """, unsafe_allow_html=True)
            except ValueError: st.error("INPUT_ERROR: NUMBERS ONLY")

# --- FOOTER ---
st.divider()
st.caption(f"{BRAND_NAME} // SECURE_ID: {USER_KEY[:5]}***")
