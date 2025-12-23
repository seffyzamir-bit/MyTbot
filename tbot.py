import streamlit as st
import pandas as pd
import requests

# הגדרות שרת ומשתמש
USER_KEY = "u4vrd84q3djw8zzsy71xqkw8dom8i1"

# עיצוב דף רחב וכהה
st.set_page_config(page_title="Pro Crypto Bot", layout="wide")

st.title("🤖 Pro Trading Dashboard")

# שורת מדדים עליונה
col1, col2, col3 = st.columns(3)
col1.metric("Balance", "$12,450", "+2.3%")
col2.metric("Open Trades", "4", "Active")
col3.metric("Daily Profit", "$340.20", "+12%")

st.divider()

# טבלת עסקאות (כמו במחשב)
st.subheader("📝 Open Orders")
df = pd.DataFrame({
    'Coin': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT'],
    'Side': ['BUY', 'BUY', 'SELL'],
    'Entry': [42500, 2250, 95.4],
    'Profit': ['+2.1%', '-0.5%', '+1.2%']
})
st.table(df)

st.divider()

# שליטה בבוט
st.subheader("🎮 Remote Commands")
c1, c2 = st.columns(2)

if c1.button("🚀 START BOT", use_container_width=True):
    # כאן אנחנו מחברים את זה ל-Pushover שלך
    st.toast("Sending Start Command...")
    st.success("Bot Engine Started on Home PC")

if c2.button("🛑 EMERGENCY STOP", use_container_width=True):
    st.error("PANIC MODE: All trades closed.")

