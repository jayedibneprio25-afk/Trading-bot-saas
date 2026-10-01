import streamlit as st
import requests

API_URL = "https://pro-trading-bot-saas.onrender.com"

st.set_page_config(page_title="SaaS Bot Admin Panel", layout="wide")
st.title("🛡️ SaaS Trading Bot - Admin & Trading Control Panel")
st.markdown("---")

# --- Section 1: Trading Execution Test ---
st.subheader("⚡ Live Paper Trading Test")
col_lic, col_act = st.columns(2)

with col_lic:
    trade_key = st.text_input("License Key for Trade", value="PRO-AMIR-2026")

with col_act:
    st.write("Execute Signal")
    btn_buy = st.button("🚀 Trigger BUY Signal")
    btn_sell = st.button("🔻 Trigger SELL Signal")

if btn_buy:
    res = requests.post(f"{API_URL}/trigger-trade/{trade_key}/BUY").json()
    if res.get("status"):
        st.success(f"BUY Executed at ${res['data']['price']:,.2f}")
        st.json(res)
    else:
        st.error(res.get("message"))

if btn_sell:
    res = requests.post(f"{API_URL}/trigger-trade/{trade_key}/SELL").json()
    if res.get("status"):
        st.info(f"SELL Executed at ${res['data']['price']:,.2f}")
        st.json(res)
    else:
        st.error(res.get("message"))

st.markdown("---")

# --- Section 2: License Management ---
st.subheader("🔑 Generate New License Key")
col1, col2, col3 = st.columns(3)

with col1:
    new_key = st.text_input("License Key", value="PRO-TEST-2026")
with col2:
    tier_option = st.selectbox("Tier", ["Pro", "Free"])
with col3:
    expiry_date = st.date_input("Expiry Date")

if st.button("Add/Update License"):
    payload = {
        "key": new_key,
        "tier": tier_option,
        "expires": str(expiry_date)
    }
    try:
        response = requests.post(f"{API_URL}/add-license", json=payload)
        if response.status_code == 200:
            st.success(f"License Key `{new_key}` synced to Backend Server!")
        else:
            st.error("Failed to sync license with Backend Server.")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

st.markdown("---")

# --- Section 3: Verification Test ---
st.subheader("🔍 Quick License Verification Test")
test_key_input = st.text_input("Enter Key to Verify", value=new_key)
if st.button("Verify Key via API"):
    try:
        res = requests.get(f"{API_URL}/verify-license/{test_key_input}").json()
        st.json(res)
    except Exception as e:
        st.error(f"API Error: {e}")