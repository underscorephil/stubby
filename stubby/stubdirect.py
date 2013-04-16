from __future__ import with_statement
from flask import Blueprint
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Blueprint
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from contextlib import closing
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from pprint import pprint as pp

blueprint = Blueprint('stubdirect', __name__)


@blueprint.route('/<stub>')
def redirect_stub(stub):
    g.db.execute('insert into requests (remote_addr, stub) values (?, ?)',
        [request.remote_addr, request.path])
    stub = Stub.get(stub)
    if stub:
        return redirect(stub.url_source)
    else:
        flash("Stub not found")
        return redirect(url_for("admin.stubs"))
