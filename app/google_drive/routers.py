from app import app

from flask import make_response
import flask

from .utils import (get_credentials,
                    get_authorization_url_ans_store_state,
                    fetch_and_store__credentials,
                    get_files)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'app/google_drive/credentials.json'


@app.route('/authorize/google_drive')
def authorize():
    credentials = get_credentials(2)
    if credentials is not None:
        return make_response({'token': credentials.token}, 200)
    url = get_authorization_url_ans_store_state(2)

    return make_response({'authorization_url': url}, 200)


@app.route('/oauth2callback/google_drive')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # # verified in the authorization server response.
    state = flask.request.args.get('state')
    fetch_and_store__credentials(state, flask.request.url)

    return 'fine'


@app.route('/files/<user_id>')
def files(user_id):
    return get_files(user_id)
