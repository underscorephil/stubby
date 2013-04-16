from flask import Blueprint
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Blueprint
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from contextlib import closing
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from stubby import User, Stub
from pprint import pprint as pp

blueprint = Blueprint('admin', __name__)


login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please login to access this feature"
login_manager.refresh_view = "reauth"



class SubsAddForm(Form):
    url_source = TextField('Source URL')
    url_stub = TextField('Stub URL')


class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')


class UserAddForm(Form):
    username = TextField('Username')
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Repeat Password')
    email = TextField('Email', [
        validators.Required(),
        validators.EqualTo('confirm_email', message='Emails do not match')
    ])
    confirm_email = TextField('Repeat email')


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@blueprint.route('/')
@login_required
def stubs():
    form = SubsAddForm(request.form)
    cur = g.db.execute('select url_source, url_stub, create_date from stubs order by create_date')
    stubs = [dict(url_source=row[0], url_stub=row[1]) for row in cur.fetchall()]
    return render_template('stubs.html', stubs=stubs, form=form)


@blueprint.route('/admin/stubs/add', methods=['POST'])
@login_required
def stubs_add():
    form = SubsAddForm(request.form)
    stub = Stub(form.url_source.data, form.url_stub.data)
    if stub.add():
        flash("Stub %s created..." % stub.url_stub)
        return redirect(url_for("stubs"))
    flash("Stub not created...")
    return redirect(url_for("stubs"))


@blueprint.route("/admin/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        # login and validate the user...
        cur = g.db.execute('select password from users where username=? LIMIT 1',
            [form.username.data])
        db_user = cur.fetchone()
        if not db_user:
            flash("Login unsucessful")
            return redirect(url_for('login'))
        if str(db_user[0]) == form.password.data:
            user = User(form.username.data, form.password.data)
            if login_user(user):
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for("stubs"))
            else:
                flash("Login unsucessful")
                return redirect(url_for("login"))
        else:
            flash("Login failed...")
            return redirect(url_for("login"))
    return render_template("/admin/login.html", form=form)


@blueprint.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("stubs"))


@blueprint.route("/admin/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("stubs"))
    return render_template("reauth.html")


@blueprint.route("/user/add", methods=["GET", "POST"])
@login_required
def user_add():
    form = UserAddForm(request.form)
    if request.method == 'POST' and form.validate():
        g.db.execute('insert into users (username, password, email) values (?, ?, ?)',
            [request.form['username'], request.form['password'], request.form['email']])
        g.db.commit()
        flash('User added...')
    return render_template("add.html", form=form)
