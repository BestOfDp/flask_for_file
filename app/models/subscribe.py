from .base import Base
from app.db import db
from app.libs.spilt_point import spilt_point


class Subscribe(Base):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.relationship('User')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book = db.relationship('Books')
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    def keys(self):
        return ['id', 'owner_id', 'book_publish', 'book_author', 'book_title', 'book_id']

    def __getitem__(self, item):
        if 'book_' in item:
            one, two = spilt_point(item, key='_')
            return getattr(getattr(self, one), two)
        else:
            return getattr(self, item)
