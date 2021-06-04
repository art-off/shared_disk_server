from app import db


class ProjectProtocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    start_time = db.Column(db.DATETIME, nullable=True, default=None)
    end_time = db.Column(db.DATETIME, nullable=True, default=None)
