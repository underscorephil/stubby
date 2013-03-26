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

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/admin')
def show_entries():
    cur = g.db.execute('select uri, short_url from entries order by id desc')
    entries = [dict(uri=row[0], short_url=row[1]) for row in cur.fetchall()]
    return render_template('display_links.html', entries=entries)

@app.route('/<short_url>')
def redirect_short_url(short_url):
    cur = g.db.execute('select uri from entries where short_url="%s"' % short_url)
    url = str(cur.fetchone()[0])
    return redirect(url)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (uri, short_url) values (?, ?)',
                 [request.form['uri'], request.form['short_url']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        # login and validate the user...
        user = User(form.username.data, form.password.data)
        login_user(user) # the user object from DB
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("admin"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

class LoginForm():
    username = TextField('Username')
    password = TextField('Password')


class User(username, password, email):
    self.username = username
    self.password = password
    self.email = email

    def login(self, username, password):
        ## sql look up compare with vars

    def get(self, userid):
        ## sql look up get user object, id, username, email

if __name__ == '__main__':
    app.run()


        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run()

