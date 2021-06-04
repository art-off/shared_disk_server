from app import db


class CreateEditFileFolderTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(db.Integer)

    file_name = db.Column(db.String(256))
    file_id = db.Column(db.Integer)

    create_or_edit_or_delete = db.Column(db.Integer)
    folder_or_file = db.Column(db.Integer)

    datetime = db.Column(db.DATETIME)

    user_type = db.Column(db.String(128))
    user_id = db.Column(db.Integer)


class VisitFolderTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(db.Integer)

    folder_name = db.Column(db.String)
    folder_id = db.Column(db.String)

    datetime = db.Column(db.DATETIME)

    user_type = db.Column(db.String(128))
    user_id = db.Column(db.Integer)
