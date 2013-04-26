from flask import request, redirect, flash, url_for
from stubby.models import Stub
from stubby.utils.db import get_url_db
from flask.ext.login import UserMixin

from stubby.utils.sessions import get_session_manager
login_manager = get_session_manager()

def redirect_stub(stub=None):
    stub = Stub.get(stub)
    if stub:
        stub.log(request.remote_addr)
        return redirect(stub.url_source)
    else:
        flash("Stub not found")
        return redirect(url_for("index"))


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
        db = get_url_db()
        cur = db.execute('select username, email from users where id=?',
            [user_id])
        db_user = str(cur.fetchone()[0])
        new_user = self(db_user[0], "", db_user[1])
        new_user.is_valid = True
        new_user.id = user_id
        return new_user
