# auth_utils.py

from google.oauth2 import credentials
from google.auth.transport.requests import Request
import os


# Define the function in this module
def get_credentials_from_refresh_token(refresh_token):
    # You should replace these with your actual client ID and client secret
    CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    TOKEN_URI = "https://oauth2.googleapis.com/token"

    creds = credentials.Credentials(
        None,  # No initial access token
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )

    # Refresh the credentials
    request = Request()
    creds.refresh(request)

    return creds
