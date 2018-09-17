from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy import orm

from .base import Base
from app.db import db
from app.api.v1.libs.enum import AuthEnum
from app.libs.save_file import save


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    _password = db.Column('password', db.String(255))
    class_name = db.Column(db.String(255))
    t_name = db.Column(db.String(255))
    photo_url = db.Column(db.String(255), default='default.png')
    email = db.Column(db.String(255))
    auth = db.Column(db.Integer, default=0)

    """
    创建对象时可以调用init
    """

    # @orm.reconstructor
    # def __init__(self, **kwargs):
    #     for o in kwargs:
    #         setattr(self, o, kwargs[o])
    #     self.show_field = []
    #     keys = getattr(self, '__dict__').keys()
    #     for key in keys:
    #         self.show_field.append(key)
    #     for o in current_app.config['MODEL_NOT_SHOW']:
    #         if o in self.show_field:
    #             self.show_field.remove(o)
    #     if '_password' in self.show_field:
    #         self.show_field.remove('_password')

    def keys(self):
        return ['name', 'id', 'email', 'photo_url', 't_name', 'class_name', 'create_time', 'auth']

    def __getitem__(self, item):
        if item == 'auth':
            return [getattr(self, item), AuthEnum(getattr(self, item)).name]
        else:
            return getattr(self, item)

    # 不返回字段
    def hide(self, *keys):
        for key in keys:
            self.show_field.remove(key)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_pwd(self, pwd):
        return check_password_hash(self.password, pwd)

    def get_auth_token(self, password=None, expires_in=None):
        if expires_in is None:
            expires_in = current_app.config['EXPIRES_IN']
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({
            'uid': self.id,
            'password': password
        }).decode('ascii')

    @staticmethod
    def check_new_name(raw):
        user = User.query.filter_by(name=raw).first()
        return True if user else False

    def save_file(self, filename, file, type, public=True):
        save(self, filename, file, type, public, replace=True)
