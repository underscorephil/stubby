# all the imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Blueprint
from wtforms import Form, BooleanField, TextField, PasswordField, validators

from contextlib import closing
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from pprint import pprint as pp

DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'


redirect_module = Blueprint('redirect', __name__, template_folder='templates')
admin_module = Blueprint('admin', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.register_blueprint(admin_module, url_prefix='/admin')
app.register_blueprint(redirect_module, url_prefix='/')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


class Stub():
    def __init__(self, url_source=None, url_stub=None):
        self.url_source = url_source
        self.url_stub = url_stub

    def add(self):
        g.db.execute('insert into stubs (url_source, url_stub) values (?, ?)',
            [self.url_source, self.url_stub])
        try:
            g.db.commit()
            flash("Stub %s Added" % self.url_stub)
            return True
        except:
            flash("Stub creation failed")
            return False

    @classmethod
    def get(self, url_stub):
        stub = False
        cur = g.db.execute('select url_source, url_stub from stubs where url_stub=?',
            [url_stub])
        res = cur.fetchone()
        if res:
            stub = self(res[0], res[1])
        return stub

    def remove(self):
        g.db.execute('delete from stubs where url_stub=? and url_source=?',
            [self.url_stub, self.url_source])
        try:
            g.db.commit()
            return True
        except:
            return False

    def log(self):
        # log request
        return


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


class User(UserMixin):
    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = 1
        self.is_valid = False

    def is_authenticated(self):
        return self.is_valid

    def is_active(self):
        ## sql look up compare with vars and set ID
        return True

    @classmethod
    def get(self, user_id):
        ## db grab that user
        cur = g.db.execute('select username, email from users where id=?',
            [user_id])
        db_user = str(cur.fetchone()[0])
        new_user = self(db_user[0], "", db_user[1])
        new_user.is_valid = True
        new_user.id = user_id
        return new_user


if __name__ == '__main__':
    app.run()
