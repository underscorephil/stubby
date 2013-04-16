# all the imports
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Blueprint
from wtforms import Form, BooleanField, TextField, PasswordField, validators

from contextlib import closing
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from db import connect_db
from pprint import pprint as pp

DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'


import admin
import stubdirect
import db
import stub
import stubuser

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.register_blueprint(admin.blueprint, url_prefix='/admin')
app.register_blueprint(stubdirect.blueprint)
app.register_blueprint(db.blueprint)
app.register_blueprint(stub.blueprint)
app.register_blueprint(stubuser.blueprint)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
    app.run(host='0.0.0.0')
