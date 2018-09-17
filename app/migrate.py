import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager

from app.db import db
from app import create_app

from app.models.user import User
from app.models.books import Books
from app.models.file import File
from app.models.subscribe import Subscribe
from app.models.blog import Blog

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
