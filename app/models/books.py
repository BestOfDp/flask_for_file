from .base import Base
from app.db import db


class Books(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    publish = db.Column(db.String(255), nullable=True)

    def keys(self):
        return ['id', 'title', 'author', 'publish']
