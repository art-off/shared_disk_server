import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    OAUTH_GOOGLE_REDIRECT_URL = 'https://artoff.bpi18.ru/oauth2callback/google_drive'

