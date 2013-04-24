from flask import Flask
from db import get_stats_db, get_url_db, close_stats_db, close_url_db
from admin import blueprint as admin_app

DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.register_blueprint(admin_app, url_prefix='/admin')


@app.before_request
def before_request():
    get_stats_db()
    get_url_db()


@app.teardown_request
def teardown_request(exception):
    close_stats_db()
    close_url_db()
