from flask import Flask as _Flask
from flask_cors import CORS
from .db import db
from flask.json import JSONEncoder as _JSONEncoder
from datetime import datetime
from flask_mail import Mail

from app.api.v1.libs.error import ResourcesException


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        elif isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            raise ResourcesException()


class Flask(_Flask):
    json_encoder = JSONEncoder


mail = Mail()


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    register_blueprint(app)
    db.init_app(app)
    mail.init_app(app)

    return app


def register_blueprint(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
