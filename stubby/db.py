from flask import g, Blueprint, current_app, app
from contextlib import closing
import sqlite3

blueprint = Blueprint('db', __name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('../schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
