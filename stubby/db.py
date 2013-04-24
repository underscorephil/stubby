from contextlib import closing
import sqlite3

blueprint = Blueprint('db', __name__)


def gattr(attr_name):
    """ lazy loads attributes onto flask.g and treats flask.g as a cache."""
    attr_name = str(attr_name)

    def inner_wrapper(f):
        def wrapper(*args, **kwargs):
            if not hasattr(g, attr_name) or not getattr(g, attr_name):
                setattr(g, attr_name, f(*args, **kwargs))
            return getattr(g, attr_name)
        return wraps(f)(wrapper)
    return inner_wrapper


@gattr('stats_db')
def get_stats_db():
    return sqlite3.connect(current_app.config['DATABASE'])


@gattr('url_db')
def get_url_db():
    return sqlite3.connect(current_app.config['DATABASE'])


def close_url_db():
    db = get_url_db()
    db.close()


def close_stats_db():
    db = get_stats_db()
    db.close()


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('../schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
