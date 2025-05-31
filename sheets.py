from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME
from creds import decode_and_save_google_credentials
from logger import logger

def append_to_google_sheet(rows):
    try:
        cred_path = decode_and_save_google_credentials()
        creds = Credentials.from_service_account_file(cred_path, scopes=[
            'https://www.googleapis.com/auth/spreadsheets'])
        service = build('sheets', 'v4', credentials=creds)
        body = {"values": rows}
        service.spreadsheets().values().append(
            spreadsheetId=GOOGLE_SHEET_ID,
            range=f"{GOOGLE_SHEET_NAME}!A:J",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
    except Exception as e:
        logger.error("Sheet append error: %s", str(e), exc_info=True)
