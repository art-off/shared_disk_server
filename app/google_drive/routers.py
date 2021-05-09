from app import app

from flask import make_response, request
import flask

from .utils import (get_credentials,
                    get_authorization_url_ans_store_state,
                    fetch_and_store__credentials,
                    get_files)

from ..auth_utils import token_auth, get_token


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'app/google_drive/credentials.json'


@app.route('/authorize/google_drive')
@token_auth.login_required
def authorize():
    token = get_token(request)
    credentials = get_credentials(token)
    if credentials is not None:
        return make_response({'token': credentials.token}, 200)
    url = get_authorization_url_ans_store_state(token)

    return make_response({'authorization_url': url}, 200)


@app.route('/oauth2callback/google_drive')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # # verified in the authorization server response.
    state = flask.request.args.get('state')
    fetch_and_store__credentials(state, flask.request.url)

    return 'fine'


@app.route('/files')
@token_auth.login_required
def files():
    token = get_token(request)
    return get_files(token)
