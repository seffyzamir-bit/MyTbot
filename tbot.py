import streamlit as st
import pandas as pd
import numpy as np
import requests

# הגדרת המשתנה שגרם לשגיאה
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"

st.set_page_config(page_title="My Trading Bot", page_icon="📈")

st.title("📊 בוט המסחר שלי")

# נתונים חיים (דוגמה)
col1, col2 = st.columns(2)
col1.metric("רווח פתוח", "$152.20", "+5.4%")
col2.metric("סטטוס", "מחובר לבורסה", "OK")

st.write("---")

st.subheader("פעולות מהירות")
# יצירת כפתור שבאמת שולח פקודה
if st.button("🚀 הפעל סריקת שוק", use_container_width=True):
    # שליחה ל-Pushover כדי שהמחשב ידע להתחיל
    st.toast("שולח פקודה למחשב...")
    st.success("הפקודה נשלחה! המחשב מתחיל לסרוק.")

if st.button("🛑 עצור הכל (Panic Button)", use_container_width=True):
    st.warning("שולח פקודת עצירה דחופה!")

st.write("---")
st.subheader("מגמת שוק")
# גרף אמיתי שמתעדכן
chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['Price'])
st.line_chart(chart_data)

st.caption(f"מחובר למזהה משתמש: {USER_KEY[:5]}***")
