from flask import g, app, Blueprint, current_app
from contextlib import closing
import sqlite3
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)


blueprint = Blueprint('stubuser', __name__)

login_manager = LoginManager()
login_manager.setup_app(blueprint)

login_manager.login_view = "login"
login_manager.login_message = "Please login to access this feature"
login_manager.refresh_view = "reauth"


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


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
