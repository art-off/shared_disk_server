from app import db

from hashlib import md5


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        bytes_password = bytes(password, encoding='utf-8')
        self.password_hash = md5(bytes_password).hexdigest()

    def check_password(self, password):
        bytes_password = bytes(password, encoding='utf-8')
        return self.password_hash == md5(bytes_password).hexdigest()
