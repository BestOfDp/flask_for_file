from datetime import datetime

from app.db import db


class Base(db.Model):
    __abstract__ = True
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def delete(self):
        self.status = 0

    def __getitem__(self, item):
        return getattr(self, item)
