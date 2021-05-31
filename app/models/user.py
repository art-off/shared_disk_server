from app import db

from .credentials import Credentials

from hashlib import md5


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(128))
    google_auth_state = db.Column(db.String(255))
    credentials_id = db.Column(db.Integer, db.ForeignKey(Credentials.id))
    credentials = db.relationship(Credentials, foreign_keys=credentials_id)

    def set_password(self, password):
        bytes_password = bytes(password, encoding='utf-8')
        self.password_hash = md5(bytes_password).hexdigest()

    def check_password(self, password):
        bytes_password = bytes(password, encoding='utf-8')
        return self.password_hash == md5(bytes_password).hexdigest()