from . import app

from flask import request, make_response

from .utils import register_user, auth_user


@app.route('/registration', methods=['POST'])
def registration():
    name = request.json.get('name')
    password = request.json.get('password')

    error = register_user(name, password)
    if error is not None:
        return make_response({'error': error}, 404)
    return make_response({'status': 'user created'}, 200)


@app.route('/auth', methods=['POST'])
def auth():
    name = request.json.get('name')
    password = request.json.get('password')

    token, error = auth_user(name, password)
    if error is not None:
        return make_response({'error': error}, 404)

    return make_response({'token': token}, 200)

