from kiteconnect import KiteConnect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet(sheet_name: str):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_google_credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def get_keys_from_sheet(sheet):
    records = sheet.get_all_records()
    return {record['key']: record['value'] for record in records}

def update_access_token(sheet, access_token):
    sheet.update_cell(3, 2, access_token)  # assuming access_token is row 3, col 2

def generate_login_url(api_key):
    kite = KiteConnect(api_key=api_key)
    return kite.login_url()

def exchange_token(api_key, api_secret, request_token):
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret=api_secret)
    return data["access_token"]
from kiteconnect import KiteConnect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet(sheet_name: str):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_google_credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def get_keys_from_sheet(sheet):
    records = sheet.get_all_records()
    return {record['key']: record['value'] for record in records}

def update_access_token(sheet, access_token):
    sheet.update_cell(3, 2, access_token)  # assuming access_token is row 3, col 2

def generate_login_url(api_key):
    kite = KiteConnect(api_key=api_key)
    return kite.login_url()

def exchange_token(api_key, api_secret, request_token):
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret=api_secret)
    return data["access_token"]
import streamlit as st
from auth import get_google_sheet, get_keys_from_sheet, generate_login_url, exchange_token, update_access_token

# Sidebar
st.sidebar.title("🔐 Zerodha Authentication")

# Connect to Google Sheet
sheet = get_google_sheet("ZerodhaTokens")  # Your Google Sheet name
creds = get_keys_from_sheet(sheet)

# Show Login URL
login_url = generate_login_url(creds["api_key"])
st.sidebar.markdown(f"[Click here to login to Zerodha]({login_url})")

# Get Request Token
request_token = st.sidebar.text_input("Paste request token from login URL")

if st.sidebar.button("🔁 Generate Access Token"):
    try:
        access_token = exchange_token(creds["api_key"], creds["api_secret"], request_token)
        update_access_token(sheet, access_token)
        st.sidebar.success("Access token saved successfully to Google Sheet ✅")
    except Exception as e:
        st.sidebar.error(f"Failed to generate token: {e}")
