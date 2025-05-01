import streamlit as st
import json
from auth import get_google_sheet

json_key = st.secrets["google_sheets"]
sheet_url = "https://docs.google.com/spreadsheets/d/your_sheet_id_here"
sheet = get_google_sheet(sheet_url, json_key)
st.write("✅ Secret loaded:", st.secrets["google_sheets"]["client_email"])
