"""OPTIONAL helper to get a YouTube refresh token on your own computer.

(The README also explains a no-code way using Google's OAuth Playground.)

1. pip install google-auth-oauthlib
2. Download your OAuth client file (type: Desktop app) from Google Cloud and save it
   next to this script as client_secret.json  (never commit this file)
3. python scripts/get_refresh_token.py
4. Sign in with the DEENIKIDS Google account and allow access.
5. Copy the printed refresh token into GitHub Secret YT_REFRESH_TOKEN.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nYT_REFRESH_TOKEN =", creds.refresh_token)
print("Client ID       =", creds.client_id)
