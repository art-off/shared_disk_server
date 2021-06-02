from app import app, db
import app.models as models

from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials

from typing import Optional, Any


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'app/google_drive/credentials.json'


def get_credentials(user_token: str) -> Optional[google.oauth2.credentials.Credentials]:
    user = __get_user_by_token(user_token)

    if user.credentials is None:
        return None

    return google.oauth2.credentials.Credentials(user.credentials.token)


def get_authorization_url_ans_store_state(user_token: str) -> str:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = app.config['OAUTH_GOOGLE_REDIRECT_URL']

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    curr_user = __get_user_by_token(user_token)
    if curr_user is not None:
        curr_user.google_auth_state = state
        db.session.add(curr_user)
        db.session.commit()

    return authorization_url


def fetch_and_store__credentials(state: str, request_url: Any) -> None:
    curr_user = __get_user_by_state(state)
    if curr_user is None:
        return None

    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = app.config['OAUTH_GOOGLE_REDIRECT_URL']

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request_url.replace('http://', 'https://', 1)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = __db_credentials_from_response(flow.credentials)
    curr_user.credentials = credentials
    db.session.add(curr_user)
    db.session.commit()


def __db_credentials_from_response(credentials: google.oauth2.credentials.Credentials) -> models.Credentials:
    return models.Credentials(token=credentials.token,
                              refresh_token=credentials.refresh_token,
                              expiry=credentials.expiry,
                              expired=credentials.expired,
                              token_uri=credentials.token_uri,
                              scopes=' '.join(credentials.scopes))


def __get_user_by_token(token):
    user = models.Manager.query.filter_by(token=token).first()

    if user is None:
        user = models.Worker.query.filter_by(token=token).first

    return user


def __get_user_by_state(state):
    user = models.Manager.query.filter_by(google_auth_state=state).first()

    if user is None:
        user = models.Worker.query.filter_by(google_auth_state=state).first

    return user