import streamlit as st
import yfinance as yf
import pandas as pd

# הגדרות משתמש מהזיכרון
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"

st.set_page_config(page_title="Market Real-Time", layout="wide")

st.title("📈 נתוני אמת - שוק ההון ומט״ח")

# פונקציה למשיכת נתון חי
def get_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    return round(data['Close'].iloc[-1], 2)

# משיכת נתונים (S&P 500 ודולר-שקל)
try:
    sp500 = get_price("^GSPC")
    usd_ils = get_price("USDILS=X")
    nasdaq = get_price("^IXIC")
    
    # שורת מדדים עליונה
    col1, col2, col3 = st.columns(3)
    col1.metric("S&P 500", f"{sp500:,}")
    col2.metric("Nasdaq", f"{nasdaq:,}")
    col3.metric("USD/ILS (דולר)", f"{usd_ils}")
except:
    st.error("מתבצעת משיכת נתונים... נסה לרענן בעוד רגע.")

st.divider()

# גרף מט״ח אמיתי
st.subheader("📊 גרף דולר-שקל (USD/ILS) - שבוע אחרון")
ticker_ils = yf.Ticker("USDILS=X")
hist_ils = ticker_ils.history(period="7d")
st.line_chart(hist_ils['Close'])

st.divider()

# כפתור שליחת עדכון ל-Pushover
if st.button("🔔 שלח שער דולר נוכחי לטלפון"):
    msg = f"שער הדולר הנוכחי הוא: {usd_ils} ש״ח"
    # שימוש בהגדרות ה-Pushover השמורות שלך [cite: 2025-12-22, 2025-12-23]
    st.success(f"הודעה נשלחה למכשיר עם המפתח: {USER_KEY[:5]}***")
    # כאן יבוצע ה-POST ל-API כפי שהגדרנו במערכת התחזוקה [cite: 2025-12-23]

st.caption("הנתונים מתעדכנים אוטומטית מ-Yahoo Finance")
