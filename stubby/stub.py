from flask import g, app, Blueprint, current_app
from contextlib import closing
import sqlite3

blueprint = Blueprint('stub', __name__)


class Stub():
    def __init__(self, url_source=None, url_stub=None):
        self.url_source = url_source
        self.url_stub = url_stub

    def add(self):
        g.db.execute('insert into stubs (url_source, url_stub) values (?, ?)',
            [self.url_source, self.url_stub])
        try:
            g.db.commit()
            flash("Stub %s Added" % self.url_stub)
            return True
        except:
            flash("Stub creation failed")
            return False

    @classmethod
    def get(self, url_stub):
        stub = False
        cur = g.db.execute('select url_source, url_stub from stubs where url_stub=?',
            [url_stub])
        res = cur.fetchone()
        if res:
            stub = self(res[0], res[1])
        return stub

    def remove(self):
        g.db.execute('delete from stubs where url_stub=? and url_source=?',
            [self.url_stub, self.url_source])
        try:
            g.db.commit()
            return True
        except:
            return False

    def log(self):
        # log request
        return
