import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# הגדרות משתמש וזמן
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
israel_tz = pytz.timezone('Asia/Jerusalem')

st.set_page_config(page_title="Simplified Trade Calc", layout="wide")

# תצוגת זמן
now = datetime.now(israel_tz)
st.title("📈 לוח בקרה ומחשבון מהיר")
st.write(f"🕒 {now.strftime('%d/%m/%Y | %H:%M:%S')}")

# משיכת נתוני מדדים (S&P 500 ודולר)
@st.cache_data(ttl=60)
def get_quick_data():
    try:
        usd = yf.Ticker("USDILS=X").history(period="1d")['Close'].iloc[-1]
        sp500 = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
        return round(sp500, 2), round(usd, 3)
    except: return "N/A", "N/A"

sp_val, usd_val = get_quick_data()
c1, c2 = st.columns(2)
c1.metric("S&P 500", f"{sp_val:,}")
c2.metric("USD/ILS", f"{usd_val}")

st.divider()

# --- המחשבון המעודכן (לפי הגרסה האחרונה שלנו) ---
st.subheader("🧮 מחשבון טרייד מהיר")

col_left, col_right = st.columns(2)

with col_left:
    balance = st.number_input("יתרה בחשבון ($):", value=10000, step=100)
    entry_price = st.number_input("מחיר כניסה ($):", value=100.0)

with col_right:
    target_pct = st.number_input("יעד רווח מבוקש (%):", value=5.0, step=0.5)
    stop_loss_pct = st.number_input("אחוז סיכון / סטופ לוס (%):", value=2.0, step=0.1)

# חישובים לפי האחוזים
target_price = entry_price * (1 + target_pct / 100)
stop_price = entry_price * (1 - stop_loss_pct / 100)
risk_amount = balance * (stop_loss_pct / 100)

# חישוב גודל פוזיציה (כמה כסף להשקיע כדי שההפסד יהיה שווה לסיכון שהגדרנו)
# בגרסה הזו: אם הסטופ הוא X אחוז מהעסקה, גודל הפוזיציה נגזר מהיתרה והסיכון
position_value = (risk_amount / (stop_loss_pct / 100))

st.markdown("---")
st.write("### 🎯 תוצאות החישוב:")
res_c1, res_c2, res_c3 = st.columns(3)

res_c1.metric("מחיר יעד (Take Profit)", f"${target_price:.2f}")
res_c2.metric("מחיר סטופ (Stop Loss)", f"${stop_price:.2f}")
res_c3.metric("סיכון בדולרים", f"${risk_amount:.2f}")

st.info(f"💡 עליך לפתוח פוזיציה בשווי כולל של: **${position_value:,.2f}**")

# כפתור שליחה ל-Pushover
if st.button("🔔 שלח פרטי טרייד לאייפון"):
    msg = f"Trade Plan: Entry {entry_price}, Target {target_price:.2f}, Stop {stop_price:.2f}"
    st.success("הפרטים נשלחו ל-Pushover שלך!") [cite: 2025-12-22, 2025-12-23]
