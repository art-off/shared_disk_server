from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# from .models import User, Credentials
from datetime import datetime
# c = Credentials(token='token2', refresh_token='reftok1', expiry=datetime.now(), expired=False, token_uri='hello', scopes='scope')
# user = User(name='name1', google_token='sldkf', credentials=c)
# db.session.add(user)
# db.session.commit()

# print(Credentials.query.all())
# print(User.query.all()[0].credentials_id)
# print('hello2')
from .google_drive import routers
