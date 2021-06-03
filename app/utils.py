from .models import User
from .models import Worker, Manager, Customer, ProfessionType
from app import db
from hashlib import sha256, md5
import validators

from typing import Optional


def register_worker(name, email, password, profession_id):
    if Worker.query.filter_by(name=name).all() or Worker.query.filter_by(email=email).all():
        return 'user_already_exist'

    worker = Worker(name=name,
                    email=email,
                    profession_type=ProfessionType.query.get(profession_id),
                    token=__generate_token(name))
    worker.set_password(password)

    db.session.add(worker)
    db.session.commit()


def register_manager(name, email, password):
    if Manager.query.filter_by(name=name).all() or Manager.query.filter_by(email=email).all():
        return 'user_already_exist'

    manager = Manager(name=name,
                      email=email,
                      token=__generate_token(name))
    manager.set_password(password)

    db.session.add(manager)
    db.session.commit()


def register_customer(first_name, middle_name, last_name, email, password):
    if Customer.query.filter_by(email=email).all():
        return 'user_already_exist'

    customer = Customer(first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        email=email)
    customer.set_password(password)

    db.session.add(customer)
    db.session.commit()


# def register_user(name: str, email: str, password: str) -> Optional[str]:
#     if not name:
#         return 'name_is_empty'
#     if len(password) < 6:
#         return 'password_too_short'
#     if not validators.email(email):
#         return 'email_is_not_valid'
#     if User.query.filter_by(name=name).all() or User.query.filter_by(email=email).all():
#         return 'user_already_exist'
#
#     user = User(name=name,
#                 email=email,
#                 token=__generate_token(name))
#     user.set_password(password)
#
#     db.session.add(user)
#     db.session.commit()


def auth_user(email: str, password: str) -> (str, Optional[str], Optional[str], Optional[str], bool, Optional[str]):
    user = Manager.query.filter_by(email=email).first()
    is_manager = True
    if user is None:
        user = Worker.query.filter_by(email=email).first()
        is_manager = False

    if user is None:
        return None, None, None, None, None, 'user_does_not_exits'
    if not user.check_password(password):
        return None, None, None, None, None, 'invalid_password'

    return user.id, user.token, user.email, user.name, is_manager, None


def __generate_token(name: str) -> str:
    return sha256(
        (
            md5(name.encode('utf-8')).hexdigest() +
            md5('secret_secret_work'.encode('utf-8')).hexdigest()
        ).encode('utf-8')
    ).hexdigest()
