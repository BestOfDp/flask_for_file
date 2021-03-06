from .base import Base
from app.db import db
import os
from flask import current_app


class Blog(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    watched = db.Column(db.Integer)
    md_path = db.Column(db.String(255), unique=True)

    def keys(self):
        return ['id', 'title', 'watched', 'md_path', 'create_time']

    def __getitem__(self, item):
        if item == 'md_path':
            path = os.path.dirname(os.path.dirname(__file__)) \
                   + current_app.config['BLOG_MD_URL'] + \
                   getattr(self, item) + '.md'
            md_txt = ''
            with open(path, 'r') as fp:
                for line in fp:
                    md_txt += line
            return md_txt
        return getattr(self, item)
