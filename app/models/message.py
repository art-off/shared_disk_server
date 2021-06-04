from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    task_id = db.Column(db.Integer)
