# all the imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from wtforms import Form, BooleanField, TextField, PasswordField, validators

from contextlib import closing
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from pprint import pprint as pp

# configuration
DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



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

login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "login"


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/stubs')
def stubs():
    cur = g.db.execute('select url_source, url_stub, create_date from stubs order create_date desc')
    stubs = [dict(url_source=row[0], url_stub=row[1]) for row in cur.fetchall()]
    return render_template('stubs.html', stubs=stubs)

@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    g.db.execute('insert into stubs (url_source, url_stub) values (?, ?)',
                 [request.form['url_source'], request.form['url_stub']])
    g.db.commit()
    flash('Stub created')
    return redirect(url_for('stubs'))


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        # login and validate the user...
        cur = g.db.execute('select password from users where username="%s"' % form.username.data)
        db_user = str(cur.fetchone()[0])
        if db_user == form.password.data:
            user = User(form.username.data, form.password.data)
            if login_user(user):
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or urL_for("stubs"))

            else:
                flash("Login unsucessful")
                return redirect(url_for("login"))
        else:
            flash("Login failed...")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(urL_for("stubs"))


@app.route("/user/add", methods=["GET", "POST"])
@login_required
def user_add():
    form = UserAddForm(request.form)
    if request.method == 'POST' and form.validate():
        g.db.execute('insert into users (username, password, email) values (?, ?, ?)',
            [request.form['username'], request.form['password'], request.form['email']])
        g.db.commit()
        flash('User added...')
    return render_template("add.html", form=form)

@app.route('/<short_url>')
def redirect_short_url(short_url):
    stub = query_db('select uri from entries where short_url="%s"' % short_url)
    if stub:
        return redirect(url)
    else:
        return redirect("http://google.com")

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

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
        cur = g.db.execute('select username, email from users where id="%s"' % user_id)
        db_user = str(cur.fetchone()[0])
        new_user = self(db_user[0], "", db_user[1])
        new_user.is_valid = True
        new_user.id = user_id
        return new_user


if __name__ == '__main__':
    app.run()

