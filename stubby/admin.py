from flask import request, g, redirect, url_for, \
    render_template, flash
from wtforms import Form, TextField, PasswordField, validators
from flask.ext.login import (
    login_required, login_user, logout_user, UserMixin, confirm_login)
from db import get_url_db
from stub import Stub

#blueprint = Blueprint('admin', __name__, template_folder='templates')


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


#@blueprint.route('/')
@login_required
def stubs():
    form = SubsAddForm(request.form)
    db = get_url_db()
    cur = db.execute(
        'select url_source, url_stub, create_date '
        'from stubs order by create_date')
    stubs = [
        dict(url_source=row[0], url_stub=row[1]) for row in cur.fetchall()]
    return render_template('stubs.html', stubs=stubs, form=form)


#@blueprint.route('/admin/stubs/add', methods=['POST'])
@login_required
def stubs_add():
    form = SubsAddForm(request.form)
    stub = Stub(form.url_source.data, form.url_stub.data)
    if stub.add():
        flash("Stub %s created..." % stub.url_stub)
        return redirect(url_for("stubs"))
    flash("Stub not created...")
    return redirect(url_for("stubs"))


#@blueprint.route("/login", methods=["GET", "POST"])
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


#@blueprint.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("stubs"))


#@blueprint.route("/admin/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("stubs"))
    return render_template("reauth.html")


#@blueprint.route("/user/add", methods=["GET", "POST"])
@login_required
def user_add():
    form = UserAddForm(request.form)
    if request.method == 'POST' and form.validate():
        g.db.execute('insert into users (username, password, email) values (?, ?, ?)',
            [request.form['username'], request.form['password'], request.form['email']])
        g.db.commit()
        flash('User added...')
    return render_template("add.html", form=form)
