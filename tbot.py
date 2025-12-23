import streamlit as st
import requests
import pandas as pd
import numpy as np

# הגדרות עיצוב - שייראה כמו אפליקציה כהה ומקצועית
st.set_page_config(page_title="Trading Bot", layout="centered")

st.title("📊 בוט מסחר - לוח בקרה")

# הצגת נתונים מהירה (דוגמה שתחבר בהמשך לבוט האמיתי)
col1, col2 = st.columns(2)
col1.metric("רווח יומי", "$120.50", "+2.5%")
col2.metric("יתרה בארנק", "$4,250", "-0.8%")

st.markdown("---")

# כפתורי שליטה בבוט
st.subheader("שליטה מרחוק")
col3, col4 = st.columns(2)

if col3.button('🚀 הפעל בוט', use_container_width=True):
    # כאן אנחנו משתמשים במפתח שלך מהזיכרון
    user_key = "u4vrd84q3djw8zzsy71xqkw8dom8i1"
    msg = "הבוט הופעל בהצלחה דרך האייפון!"
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": "YOUR_APP_TOKEN", # כאן נצטרך להכניס טוקן אפליקציה בהמשך
        "user": user_key,
        "message": msg
    })
    st.success(msg)

if col4.button('🛑 עצור בוט', use_container_width=True):
    st.error("פקודת עצירה נשלחה למחשב")

# גרף דוגמה (כדי שייראה כמו תוכנת מסחר)
st.subheader("גרף מחיר בזמן אמת")
chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['Price'])
st.line_chart(chart_data)

st.info(f"מפתח Pushover מוגדר: {user_key[:5]}...") # הצגה חלקית לביטחון
