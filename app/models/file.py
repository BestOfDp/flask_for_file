from sqlalchemy import orm
from flask import g, current_app

from app.models.base import Base
from app.db import db


class File(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    format = db.Column(db.String(255))
    all_could = db.Column(db.Integer, default=0)
    del_time = db.Column(db.DateTime)

    owner = db.relationship('User')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def keys(self):
        return ['id', 'title', 'url', 'format', 'owner_id', 'create_time', 'del_time']
