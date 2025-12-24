import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# --- CORE CONFIGURATION ---
BRAND_NAME = "SZ SOLUTIONS"
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1" [cite: 2025-12-22]
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title=f"{BRAND_NAME} | OS", layout="wide")

# --- CUSTOM INDUSTRIAL DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #C0C0C0; font-family: 'Inter', sans-serif; }
    
    /* Centering and Container */
    .block-container { max-width: 800px !important; padding-top: 2rem !important; margin: auto !important; }
    
    /* SZ SOLUTIONS Modules */
    .st-emotion-cache-12w0qpk { 
        background-color: #0F0F0F; padding: 25px; border-radius: 0px; 
        border: 1px solid #1A1A1A; margin-bottom: 20px; text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Typography */
    h1 { color: #FFFFFF !important; letter-spacing: 8px; font-weight: 200 !important; text-align: center !important; border-bottom: 1px solid #1A1A1A; padding-bottom: 10px; }
    h3 { color: #808080 !important; text-transform: uppercase; letter-spacing: 3px; font-size: 14px !important; text-align: center !important; }
    
    /* Inputs - Matte Black Style */
    input { 
        background-color: #0A0A0A !important; border: 1px solid #262626 !important; 
        color: #FFFFFF !important; text-align: center !important; border-radius: 0px !important;
    }
    
    /* Buttons - Silver & Deep Green */
    .stButton>button {
        border: 1px solid #262626; background-color: #0F0F0F; color: #C0C0C0;
        letter-spacing: 1px; text-transform: uppercase; border-radius: 0px; font-size: 10px;
        transition: 0.3s; width: auto !important; min-width: 100px; margin: 5px auto !important;
    }
    .stButton>button:hover { border-color: #404040; color: #FFFFFF; background-color: #1A1A1A; }
    
    /* Risk Matrix Button - Deep Green Highlight */
    button[kind="primary"] { 
        border: 1px solid #004D00 !important; color: #00FF00 !important; 
        background-color: #051405 !important; font-weight: bold !important;
    }
    
    /* Close Button (X) */
    .close-btn { color: #404040; cursor: pointer; float: right; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- STATE ---
if 'show_matrix' not in st.session_state: st.session_state.show_matrix = False
if 'analysis_view' not in st.session_state: st.session_state.analysis_view = None

# --- HEADER (LOGO) ---
st.markdown(f"<h1>{BRAND_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#404040; font-size:10px; letter-spacing:2px;'>CORE OS // {datetime.now(israel_tz).strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# --- MODULE 01: MARKET INTELLIGENCE (INDEX TABLE) ---
with st.container():
    st.markdown("### Market Intelligence")
    indices = {
        "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "RSP": "RSP", 
        "RUSSELL 2000": "^RUT", "BITCOIN": "BTC-USD", "USD/ILS": "USDILS=X"
    }
    
    cols = st.columns(3)
    for i, (name, ticker) in enumerate(indices.items()):
        with cols[i % 3]:
            try:
                price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
                st.metric(name, f"{price:,.2f}" if "USD" not in ticker else f"{price:.3f}")
                st.markdown(f"[GO] (https://www.google.com/finance/quote/{ticker.replace('^','')})")
            except: st.caption("SYNC...")

# --- MODULE 02: SECURITY ANALYSIS (TRACKER) ---
with st.container():
    st.markdown("### Security Analysis")
    # שורת טיקר ארוכה
    target = st.text_input("TICKER", placeholder="ENTER SYMBOL (e.g. NVDA)", label_visibility="collapsed").upper()
    
    # כפתורים קטנים ממורכזים
    c1, c2, c3 = st.columns([1,1,1])
    if c1.button("LOAD CHART"): st.session_state.analysis_view = "chart"
    if c2.button("EXTRACT"): st.session_state.analysis_view = "intel"
    if c3.button("X"): st.session_state.analysis_view = None

    if st.session_state.analysis_view == "chart" and target:
        st.line_chart(yf.Ticker(target).history(period="1mo")['Close'])
    elif st.session_state.analysis_view == "intel" and target:
        st.write(yf.Ticker(target).info.get('longBusinessSummary', 'N/A'))

# --- MODULE 03: RISK MATRIX (POP-UP STYLE) ---
st.markdown("---")
if st.button("OPEN RISK MATRIX", type="primary"):
    st.session_state.show_matrix = not st.session_state.show_matrix

if st.session_state.show_matrix:
    with st.container():
        st.markdown("### Risk Matrix")
        m1, m2, m3 = st.columns(3)
        # ערכים מוטבעים בתוך השורה
        entry = m1.text_input("ENT", placeholder="ENTRY $")
        tp = m2.text_input("TP", placeholder="TARGET %")
        sl = m3.text_input("SL", placeholder="STOP %")
        
        if entry and tp and sl:
            e, t, s = float(entry), float(tp), float(sl)
            st.success(f"TARGET: ${e*(1+t/100):.2f} | STOP: ${e*(1-s/100):.2f} | R/R: {t/s:.1f}")

# --- FOOTER ---
st.divider()
st.caption(f"© 2025 {BRAND_NAME} | SYSTEM_ID: {USER_KEY[:5]}***") [cite: 2025-12-22, 2025-12-23]
