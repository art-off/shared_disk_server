from .models import User
from app import db
from hashlib import sha256, md5
import validators

from typing import Optional


def register_user(name: str, email: str, password: str) -> Optional[str]:
    if not name:
        return 'name_is_empty'
    if len(password) < 6:
        return 'password_too_short'
    if not validators.email(email):
        return 'email_is_not_valid'
    if User.query.filter_by(name=name).all() or User.query.filter_by(email=email).all():
        return 'user_already_exist'

    user = User(name=name,
                email=email,
                token=__generate_token(name))
    user.set_password(password)

    db.session.add(user)
    db.session.commit()


def auth_user(email: str, password: str) -> (Optional[str], Optional[str], Optional[str], Optional[str]):
    user = User.query.filter_by(email=email).first()

    print(user)
    if user is None:
        return None, None, None, 'user_does_not_exits'
    if not user.check_password(password):
        return None, None, None, 'invalid_password'

    return user.token, user.email, user.name, None


def __generate_token(name: str) -> str:
    return sha256(
        (
            md5(name.encode('utf-8')).hexdigest() +
            md5('secret_secret_work'.encode('utf-8')).hexdigest()
        ).encode('utf-8')
    ).hexdigest()
