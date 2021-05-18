from app import app

import flask
from flask import request, make_response

from ..auth_utils import token_auth, get_token

from .utils import get_credentials
from .auth_utils import (get_authorization_url_ans_store_state,
                         fetch_and_store__credentials)


@app.route('/authorize/google_drive')
@token_auth.login_required
def authorize():
    token = get_token(request)
    credentials = get_credentials(token)
    if credentials is not None:
        return make_response({'token': credentials.token}, 200)
    url = get_authorization_url_ans_store_state(token)

    return make_response({'authorization_url': url}, 200)


@app.route('/refresh_authorize/google_drive')
@token_auth.login_required
def refresh():
    token = get_token(request)
    url = get_authorization_url_ans_store_state(token)
    return make_response({'authorization_url': url}, 200)


@app.route('/oauth2callback/google_drive')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # # verified in the authorization server response.
    state = flask.request.args.get('state')
    fetch_and_store__credentials(state, flask.request.url)

    return 'fine'
