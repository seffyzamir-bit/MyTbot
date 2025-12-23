import streamlit as st
import pandas as pd
import numpy as np

# הגדרות עיצוב למראה שוק ההון
st.set_page_config(page_title="Market Monitor", layout="wide")

st.title("📈 Market Watch - מדדי חוץ")

# שורת המדדים העיקריים - נתונים לדוגמה שנעדכן לחיים
col1, col2, col3 = st.columns(3)
col1.metric("S&P 500", "5,123.40", "+1.2%")
col2.metric("Nasdaq", "16,248.50", "+0.85%")
col3.metric("Dow Jones", "39,120.10", "-0.15%")

st.divider()

# טבלת מעקב מניות/מדדים
st.subheader("📋 רשימת מעקב אישית")
watchlist = pd.DataFrame({
    'סימול': ['AAPL', 'NVDA', 'MSFT', 'TSLA'],
    'מחיר': [185.92, 875.20, 415.50, 175.30],
    'שינוי יומי': ['+0.5%', '+3.2%', '-0.2%', '-1.5%'],
    'סטטוס': ['מגמת עלייה', 'פריצה', 'דשדוש', 'תמיכה']
})
st.table(watchlist)

st.divider()

# כפתורי שליטה בהתראות (מחובר ל-Pushover שלך)
st.subheader("🔔 הגדרת התראות לטלפון")
price_target = st.number_input("הזן רף למדד S&P 500:", value=5150)

if st.button("עדכן התראה באייפון"):
    # שימוש במפתח ששמרנו עבורך
    user_key = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
    st.info(f"התראה הוגדרה. תקבל הודעה ל-Pushover ברגע שהמדד יחצה את {price_target}")
    # כאן בהמשך ירוץ הקוד ששולח את ההודעה בפועל [cite: 2025-12-23]

st.caption("מערכת מעקב שוק ההון | מחובר למכשירך u4vrd***")
