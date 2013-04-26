from flask import current_app
from stubby.utils import lazy_load
import sqlite3


@lazy_load('stats_db')
def get_stats_db():
    return sqlite3.connect(current_app.config['DATABASE'])


@lazy_load('url_db')
def get_url_db():
    return sqlite3.connect(current_app.config['DATABASE'])


def close_url_db():
    db = get_url_db()
    db.close()


def close_stats_db():
    db = get_stats_db()
    db.close()


def init_db():
    db = get_url_db()
    with current_app.open_resource('../schema.sql') as f:
        db.cursor().executescript(f.read())
    db.commit()
