import streamlit as st
from core.license_engine import license_engine

st.set_page_config(page_title="SaaS Bot Admin Panel", layout="wide")

st.title("🛡️ SaaS Trading Bot - License Management Panel")
st.markdown("---")

st.subheader("🔑 Generate New License Key")
col1, col2, col3 = st.columns(3)

with col1:
    new_key = st.text_input("License Key", value="PRO-TEST-2026")
with col2:
    tier_option = st.selectbox("Tier", ["Pro", "Free"])
with col3:
    expiry_date = st.date_input("Expiry Date")

if st.button("Add/Update License"):
    license_engine.add_or_update_license(new_key, tier_option, str(expiry_date))
    st.success(f"License Key `{new_key}` successfully saved to Database!")

st.markdown("---")

st.subheader("📋 Active License Database")
st.json(license_engine.get_all_licenses())