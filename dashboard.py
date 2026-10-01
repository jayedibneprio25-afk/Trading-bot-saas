import streamlit as st
import pandas as pd
import sqlite3
import time
from core.data_engine import data_engine
from core.trade_engine import trade_engine

st.set_page_config(page_title="Pro SaaS Trading Dashboard", layout="wide")

st.title("🤖 Pro Trading Bot SaaS - Admin & Control Panel")
st.markdown("---")

# Sidebar - Bot Controls
st.sidebar.header("⚙️ Bot Controls")
bot_status = st.sidebar.toggle("Bot Power Switch", value=True)

if bot_status:
    st.sidebar.success("Status: Engine Active 🟢")
else:
    st.sidebar.error("Status: Engine Stopped 🔴")

# Top Metrics Row
col1, col2, col3 = st.columns(3)

live_price = data_engine.get_live_price("BTCUSDT") or 0.0

col1.metric(label="BTC/USDT Live Price", value=f"${live_price:,.2f}")
col2.metric(label="Current Balance", value=f"${trade_engine.balance:,.2f}")
col3.metric(label="Active Positions", value=len(trade_engine.positions))

st.markdown("---")

# Active Positions & Database Trade History
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Active Position Details")
    if trade_engine.positions:
        st.json(trade_engine.positions)
    else:
        st.info("No active positions currently open.")

with col_right:
    st.subheader("📜 Recent Trade History")
    try:
        conn = sqlite3.connect("trading_bot.db")
        df = pd.read_sql_query("SELECT * FROM trade_history ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No trades recorded in database yet.")
    except Exception as e:
        st.error(f"Error loading trade history: {e}")