from flask_restful import Resource, reqparse, abort
from flask import g, url_for
from app.common.db.tables import Cliente as User
from app import auth, db



