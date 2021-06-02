from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)


# from .models import User, Credentials
from datetime import datetime
# c = Credentials(token='token2', refresh_token='reftok1', expiry=datetime.now(), expired=False, token_uri='hello', scopes='scope')
# user = User(name='name1', google_token='sldkf', credentials=c)
# db.session.add(user)
# db.session.commit()

# print(Credentials.query.all())
# print(User.query.all()[0].credentials_id)
# print('hello2')
from . import routers
from . import project_routers
from .google_drive import auth_routers, routers

from .models import ProfessionType, Manager, Worker, Customer, DevelopmentStageType


def add_professions_and_manager():
    m = Manager(name='art-off', email='tema27072000@gmail.com', token='123456')
    m.set_password('1234567')

    db.session.add(m)
    db.session.add(ProfessionType(name='Дизайнер'))
    db.session.add(ProfessionType(name='Разработчик'))
    db.session.add(ProfessionType(name='Тестировщик'))
    db.session.add(DevelopmentStageType(name='Дизайн'))
    db.session.add(DevelopmentStageType(name='Разработка'))
    db.session.add(DevelopmentStageType(name='Тестирование'))

    w1 = Worker(email="shareddiskworker1@gmail.com",
                name="worker1",
                profession_type=ProfessionType.query.get(1),
                token='111111')
    w1.set_password('user1pas')
    w2 = Worker(email="shareddiskworker2@gmail.com",
                name="worker2",
                profession_type=ProfessionType.query.get(2),
                token='222222')
    w2.set_password('user1pas')
    w3 = Worker(email="shareddiskworker3@gmail.com",
                name="worker3",
                profession_type=ProfessionType.query.get(3),
                token='333333')
    w3.set_password('user1pas')
    # w4 = Worker(email="shareddiskworker4@gmail.com",
    #             name="worker4",
    #             profession_type=ProfessionType.query.get(1),
    #             token='444444')
    # w1.set_password('user1pas')

    c1 = Customer(email="shareddiskcustomer3@gmail.com",
                  first_name="Костя",
                  middle_name="Николаевич",
                  last_name="Козырев")
    c1.set_password('user1pas')

    db.session.add(w1)
    db.session.add(w2)
    db.session.add(w3)
    # гугл больше не дает создавать аккаунты :(
    # db.session.add(w4)
    db.session.add(c1)

    db.session.commit()

# add_professions_and_manager()

# print('debug users added')