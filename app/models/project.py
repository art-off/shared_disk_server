from app import db

from .customer import Customer
from .manager import Manager


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    deadline = db.Column(db.DATETIME)
    start_date = db.Column(db.DATETIME)

    folder_id = db.Column(db.String(256))
    customer_folder_id = db.Column(db.String(256))

    __customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    customer = db.relationship(Customer, foreign_keys=__customer_id)

    __manager_id = db.Column(db.Integer, db.ForeignKey(Manager.id))
    manager = db.relationship(Manager, foreign_keys=__manager_id)
