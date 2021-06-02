from flask_httpauth import HTTPTokenAuth

from .models import Worker, Manager

from typing import Optional


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verity_token(token):
    worker = Worker.query.filter_by(token=token).first()
    manager = Manager.query.filter_by(token=token).first()

    if manager is not None:
        return manager.token == token
    if worker is not None:
        return worker.token == token
    return False


def get_token(request) -> Optional[str]:
    bearer = request.headers.get('Authorization')
    if bearer is None:
        return None
    word_and_token = bearer.split()
    if len(word_and_token) == 2:
        return word_and_token[1]
    return None