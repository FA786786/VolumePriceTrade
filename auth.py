# auth.py

def get_google_sheet():
    return "Dummy Google Sheet"

def get_keys_from_sheet():
    return {"api_key": "dummy_key", "secret": "dummy_secret"}

def generate_login_url():
    return "https://example.com/login"

def exchange_token():
    return "dummy_token"

def update_access_token():
    return True
import streamlit as st

def get_api_keys():
    return {
        "api_key": st.secrets["api"]["api_key"],
        "secret": st.secrets["api"]["secret"]
    }
