from app import db


class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expiry = db.Column(db.DATETIME)
    expired = db.Column(db.Boolean)
    token_uri = db.Column(db.String(255))
    scopes = db.Column(db.String)