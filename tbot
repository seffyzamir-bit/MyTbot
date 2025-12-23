import streamlit as st

st.title("הבוט שלי - לוח בקרה")

# הצגת נתונים בסיסיים
st.metric(label="סטטוס בוט", value="פעיל", delta="OK")

# כפתור פעולה
if st.button('שלח התראת בדיקה לאייפון'):
    # כאן נכניס בהמשך את הקוד שמשתמש ב-Pushover Key שלך
    st.write("שולח הודעה ל-Pushover...")
    st.success("ההודעה נשלחה בהצלחה!")

# תיבת טקסט להזנת פקודות
command = st.text_input("הזן פקודה לבוט:")
if command:
    st.write(f"הפקודה '{command}' התקבלה.")
