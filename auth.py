import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet(sheet_url, json_keyfile_dict):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_keyfile_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    return sheet
