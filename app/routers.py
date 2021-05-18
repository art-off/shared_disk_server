from . import app

from flask import request, make_response

from .utils import register_user, auth_user
from .auth_utils import token_auth, get_token


@app.route('/')
@token_auth.login_required
def hello():
    token = get_token(request)
    return token


@app.route('/registration', methods=['POST'])
def registration():
    name = request.json.get('name')
    password = request.json.get('password')

    if name is None or password is None:
        return make_response({'error': 'required params does not exist'}, 403)

    error = register_user(name, password)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'status': 'user created'}, 200)


@app.route('/auth', methods=['POST'])
def auth():
    name = request.json.get('name')
    password = request.json.get('password')

    if name is None or password is None:
        return make_response({'error': 'required params does not exist'}, 403)

    token, error = auth_user(name, password)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'token': token}, 200)

