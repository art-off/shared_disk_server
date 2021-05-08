from app import db


class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expiry = db.Column(db.DATETIME)
    expired = db.Column(db.Boolean)
    token_uri = db.Column(db.String(255))
    scopes = db.Column(db.String)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    google_auth_state = db.Column(db.String(255))
    credentials_id = db.Column(db.Integer, db.ForeignKey(Credentials.id))
    credentials = db.relationship(Credentials, foreign_keys=credentials_id)

