from app import db

from .development_stage import DevelopmentStage
from .worker import Worker


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    ready = db.Column(db.Boolean, default=False)

    folder_id = db.Column(db.String(256))
    customer_folder_id = db.Column(db.String(256))
    finally_folder_id = db.Column(db.String(256))

    __development_stage_id = db.Column(db.Integer, db.ForeignKey(DevelopmentStage.id))
    development_stage = db.relationship(DevelopmentStage, foreign_keys=__development_stage_id)

    __worker_id = db.Column(db.Integer, db.ForeignKey(Worker.id))
    worker = db.relationship(Worker, foreign_keys=__worker_id)