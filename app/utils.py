from .models import User
from app import db
from hashlib import sha256, md5

from typing import Optional


def register_user(name: str, password: str) -> Optional[str]:
    if not name:
        return 'name_is_empty'
    if len(password) < 6:
        return 'password_too_short'
    if User.query.filter_by(name=name).all():
        return 'user_already_exist'

    user = User(name=name)
    user.set_password(password)
    user.token = __generate_token(name)

    db.session.add(user)
    db.session.commit()


def auth_user(name: str, password: str) -> (Optional[str], Optional[str]):
    user = User.query.filter_by(name=name).first()

    if user is None:
        return None, 'user_does_not_exits'
    if not user.check_password(password):
        return None, 'invalid_password'

    return user.token, None


def __generate_token(name: str) -> str:
    return sha256(
        (
            md5(name.encode('utf-8')).hexdigest() +
            md5('secret_secret_work'.encode('utf-8')).hexdigest()
        ).encode('utf-8')
    ).hexdigest()
