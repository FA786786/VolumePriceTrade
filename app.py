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
