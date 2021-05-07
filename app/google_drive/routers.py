from app import app

from flask import Flask
from flask import url_for
from flask import jsonify
import flask

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .utils import get_token, get_authorization_url_ans_store_state


@app.route('/')
def hello():
    return jsonify(name='nameee', sl='lsssss')


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'app/google_drive/credentials.json'


@app.route('/authorize')
def authorize():
    token = get_token(1)
    if token is not None:
        return jsonify(token=token)

    url = get_authorization_url_ans_store_state(1)

    return {
        'authorization_url': url
    }

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # # verified in the authorization server response.
    state = flask.request.args.get('state')

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

    flow.redirect_uri = flask.url_for('oauth2callback', _external=True, _scheme='https')

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url.replace('http://', 'https://', 1)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    print(credentials_to_dict(credentials))
    # flask.session['credentials'] = credentials_to_dict(credentials)

    service = build('drive', 'v3', credentials=credentials)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    result = ''
    if not items:
        result += 'No files found.'
    else:
        result += 'Files:<br>'
        for item in items:
            result += u'{0} ({1})<br>'.format(item['name'], item['id'])

    return result


def credentials_to_dict(credentials: Credentials) -> dict:
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'expiry': credentials.expiry,
        'expired': credentials.expired,
        'token_uri': credentials.token_uri,
        'scopes': credentials.scopes
    }