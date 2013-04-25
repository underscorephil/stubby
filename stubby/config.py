from flask import Blueprint
blueprint = Blueprint('config', __name__)

DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'
