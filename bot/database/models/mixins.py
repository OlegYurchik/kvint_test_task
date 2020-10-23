import datetime

from botovod.dbdrivers.gino import db


class CommonMixin:
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now, nullable=True)
