from app import app

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow

from typing import Optional

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'app/google_drive/credentials.json'


# TODO: Сделать нормальную реализацию со взятием из БД
def get_token(user_id: int) -> Optional[str]:
    return None


def get_authorization_url_ans_store_state(user_id: int) -> str:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = app.config['OAUTH_GOOGLE_REDIRECT_URL']

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.

    return authorization_url
