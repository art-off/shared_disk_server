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

from .utils import (get_credentials,
                    get_authorization_url_ans_store_state,
                    fetch_and_store__credentials,
                    get_files)


@app.route('/')
def hello():
    return jsonify(name='nameee', sl='lsssss')


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'app/google_drive/credentials.json'


@app.route('/authorize')
def authorize():
    credentials = get_credentials(2)
    if credentials is not None:
        return jsonify(token=credentials.token)

    url = get_authorization_url_ans_store_state(2)

    return {
        'authorization_url': url
    }


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # # verified in the authorization server response.
    state = flask.request.args.get('state')
    fetch_and_store__credentials(state, flask.request.url)

    return 'fine'


@app.route('/files/<user_id>')
def files(user_id):
    return get_files(user_id)