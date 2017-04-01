from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object('config')

auth = HTTPBasicAuth()

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

api = Api(app)

from app.common.db import tables
from app import route
