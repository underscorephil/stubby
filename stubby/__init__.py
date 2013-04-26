from flask import Flask
app = Flask(__name__)

import stubby.stubuser
import stubby.admin


DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'
