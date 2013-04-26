from flask import Flask
from db import close_stats_db, close_url_db
from stubdirect import redirect_stub
from admin import stubs, login
import stubuser
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)


DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please login to access this feature"
login_manager.refresh_view = "reauth"


@app.teardown_request
def teardown_request(exception):
    close_stats_db()
    close_url_db()


def index():
    return "Hello, and welcome"


app.add_url_rule('/', 'index', index)
app.add_url_rule('/<stub>', 'stub_redirect', redirect_stub)
app.add_url_rule('/admin', 'admin', stubs)
app.add_url_rule('/login', 'login', login)
