from flask_httpauth import HTTPTokenAuth

from .models import User

from typing import Optional


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verity_token(token):
    print(token)
    user = User.query.filter_by(token=token).first()
    if user is not None:
        return user.token == token
    return False


def get_token(request) -> Optional[str]:
    bearer = request.headers.get('Authorization')
    if bearer is None:
        return None
    word_and_token = bearer.split()
    if len(word_and_token) == 2:
        return word_and_token[1]
    return None