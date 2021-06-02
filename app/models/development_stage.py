from app import db

from .project import Project


class DevelopmentStageType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)


class DevelopmentStage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    folder_id = db.Column(db.String(256))

    __project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    project = db.relationship(Project, foreign_keys=__project_id)

    __development_stage_type_id = db.Column(db.Integer, db.ForeignKey(DevelopmentStageType.id))
    development_stage_type = db.relationship(DevelopmentStageType, foreign_keys=__development_stage_type_id)
