# app.py

import os
import streamlit as st

from auth import (
    get_google_sheet,
    get_keys_from_sheet,
    generate_login_url,
    exchange_token,
    update_access_token,
)

st.set_page_config(page_title="Volume Price Trade App")

st.title("📈 Volume Price Trade App")

# Dummy usage example
st.write("Google Sheet:", get_google_sheet())
st.write("API Keys:", get_keys_from_sheet())
st.write("Login URL:", generate_login_url())
