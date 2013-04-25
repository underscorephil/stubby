from flask import Flask
from db import close_stats_db, close_url_db
from stubdirect import redirect_stub

DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)


@app.teardown_request
def teardown_request(exception):
    close_stats_db()
    close_url_db()


def index():
    return "Hello, and welcome"


app.add_url_rule('/', 'index', index)
app.add_url_rule('/<stub>', 'stub_redirect', redirect_stub)
