from flask import request, g, redirect, url_for, \
    render_template, flash
from wtforms import Form, TextField, PasswordField, validators
from flask.ext.login import (
    login_required, login_user, logout_user, UserMixin, confirm_login)
from stubby.utils.db import get_url_db
from stubby.utils.sessions import get_session_manager
from stubby.models.stub import Stub
from pprint import pprint as pp
from stubby.main import db
login_manager = get_session_manager()
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


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    


@login_required
def index():
    form = SubsAddForm(request.form)
    db = get_url_db()
    cur = db.execute(
        'select url_source, url_stub, create_date '
        'from stubs order by create_date')
    stubs = [
        dict(url_source=row[0], url_stub=row[1]) for row in cur.fetchall()]
    return render_template('stubs.html', stubs=stubs, form=form)


@login_required
def stubs_add():
    form = SubsAddForm(request.form)
    stub = Stub(form.url_source.data, form.url_stub.data)
    stub.save()
    return redirect(url_for("admin"))


@login_required
def stubs_delete(id):
    stub = Stub(url_stub=id)
    stub.delete()
    return redirect(url_for("admin"))


def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        # login and validate the user...
        db = get_url_db()
        cur = db.execute('select password from users where username=? LIMIT 1',
                         [form.username.data])
        db_user = cur.fetchone()
        if not db_user:
            flash("Login unsucessful")
            return redirect(url_for('login'))
        if str(db_user[0]) == form.password.data:
            user = User(form.username.data, form.password.data)
            if login_user(user):
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for("admin"))
            else:
                flash("Login unsucessful")
                return redirect(url_for("login"))
        else:
            flash("Login failed...")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for("admin"))


@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("admin"))
    return render_template("reauth.html")


@login_required
def user_add():
    form = UserAddForm(request.form)
    db = get_url_db()
    if request.method == 'POST' and form.validate():
        db.execute('insert into users (username, password, email) values (?, ?, ?)',
            [request.form['username'], request.form['password'], request.form['email']])
        g.db.commit()
        flash('User added...')
    return render_template("add.html", form=form)
