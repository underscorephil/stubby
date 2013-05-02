from flask import Flask
from stubby.utils.db import close_stats_db, close_url_db


DATABASE = '/tmp/redirect.db'
DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

from stubby.utils.sessions import get_session_manager
from stubby.views import admin, stub


@app.teardown_request
def teardown_request(exception):
    close_stats_db()
    close_url_db()


def index():
    return "Hello, and welcome to stubs!"

login_manager = get_session_manager()
login_manager.setup_app(app)


app.add_url_rule('/', endpoint='index', view_func=index)
app.add_url_rule('/<stub>', endpoint='stub_redirect',
                 view_func=stub.redirect_stub)

app.add_url_rule('/admin', endpoint='admin', view_func=admin.index)

app.add_url_rule('/admin/stub/add', view_func=admin.stubs_add,
                 methods=['POST'])
app.add_url_rule('/admin/stub/delete/<id>', view_func=admin.stubs_delete,
                 methods=['GET'])

app.add_url_rule('/login', endpoint='login', view_func=admin.login,
                 methods=['GET', 'POST'])

app.add_url_rule('/logout', endpoint='logout', view_func=admin.logout)




if __name__ == "__main__":
    app.run(host="0.0.0.0")
