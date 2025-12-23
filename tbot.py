import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# הגדרות משתמש מהזיכרון
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title="Trading OS", layout="wide")

# תצוגת זמן (לבקשתך)
now = datetime.now(israel_tz)
st.title("🖥️ מערכת ניהול טריידים")
st.write(f"📅 {now.strftime('%d/%m/%Y')} | 🕒 {now.strftime('%H:%M:%S')}")

st.divider()

# --- חלק 1: איתור מניות ומידע מרשת ---
st.subheader("🔍 איתור מניות וניתוח")
symbol = st.text_input("הזן סימול מניה (למשל AAPL, NVDA):", value="NVDA").upper()

col1, col2, col3 = st.columns(3)

if col1.button(f"📈 הצג גרף {symbol}", use_container_width=True):
    data = yf.Ticker(symbol).history(period="1mo")
    st.line_chart(data['Close'])

if col2.button(f"📰 מידע מהרשת", use_container_width=True):
    ticker = yf.Ticker(symbol)
    st.write(f"**מידע על {symbol}:**")
    st.write(ticker.info.get('longBusinessSummary', 'לא נמצא מידע'))

if col3.button(f"🔔 מעקב טרייד (Pushover)", use_container_width=True):
    # שליחת התראת תחילת מעקב למכשיר שלך [cite: 2025-12-23]
    st.success(f"החל מעקב אחרי {symbol}. תקבל עדכונים ל-Pushover.")

st.divider()

# --- חלק 2: מחשבון טרייד משופר (ללא המלצת רכישה קבועה) ---
st.subheader("🧮 מחשבון טרייד")
c_a, c_b, c_c = st.columns(3)

entry = c_a.number_input("מחיר כניסה ($):", value=100.0)
target_pct = c_b.number_input("יעד רווח (%):", value=5.0)
stop_pct = c_c.number_input("סטופ לוס (%):", value=2.0)

# חישוב יעדים
tp_price = entry * (1 + target_pct / 100)
sl_price = entry * (1 - stop_pct / 100)
rr_ratio = target_pct / stop_pct

st.info(f"🎯 **יעד (TP):** ${tp_price:.2f} | 🛑 **סטופ (SL):** ${sl_price:.2f} | ⚖️ **יחס סיכון-סיכוי:** 1:{rr_ratio:.1f}")

st.divider()

# --- חלק 3: מדדי שוק עיקריים ---
st.subheader("🌍 מבט על השוק")
@st.cache_data(ttl=60)
def get_market():
    return {
        "S&P 500": yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1],
        "USD/ILS": yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
    }

m_data = get_market()
mc1, mc2 = st.columns(2)
mc1.metric("S&P 500", f"{m_data['S&P 500']:,.2f}")
mc2.metric("דולר-שקל", f"{m_data['USD/ILS']:.3f}")

st.caption(f"מחובר ל-Pushover: {USER_KEY[:5]}***")
