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
        import streamlit as st
import requests
from core.license_engine import license_engine

st.set_page_config(page_title="SaaS Bot Admin Panel", layout="wide")

st.title("🛡️ SaaS Trading Bot - License Management Panel")
st.markdown("---")

# ১. নতুন লাইসেন্স কি তৈরি করার সেকশন
st.subheader("🔑 Generate New License Key")
col1, col2, col3 = st.columns(3)

with col1:
    new_key = st.text_input("License Key", value="PRO-AMIR-2026")
with col2:
    tier_option = st.selectbox("Tier", ["Pro", "Free"])
with col3:
    expiry_date = st.date_input("Expiry Date")

if st.button("Add/Update License"):
    license_engine.valid_keys[new_key] = {
        "tier": tier_option,
        "expires": str(expiry_date)
    }
    st.success(f"License Key `{new_key}` successfully configured for **{tier_option}** Tier!")

st.markdown("---")

# ২. বর্তমান লাইসেন্স ডাটাবেস টেবিল
st.subheader("📋 Active License Database")
st.json(license_engine.valid_keys)