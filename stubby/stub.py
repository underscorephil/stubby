from flask import flash
from db import get_url_db


class Stub():
    def __init__(self, url_source=None, url_stub=None):
        self.url_source = url_source
        self.url_stub = url_stub
        self.db = get_url_db()

    def add(self):
        self.db.execute('insert into stubs (url_source, url_stub) values (?, ?)',
            [self.url_source, self.url_stub])
        try:
            self.db.commit()
            flash("Stub %s Added" % self.url_stub)
            return True
        except:
            flash("Stub creation failed")
            return False

    @classmethod
    def get(self, url_stub):
        stub = False
        db = get_url_db()
        cur = db.execute('select url_source, url_stub from stubs where url_stub=?',
            [url_stub])
        res = cur.fetchone()
        if res:
            stub = self(res[0], res[1])
        return stub

    def remove(self):
        self.db.execute('delete from stubs where url_stub=? and url_source=?',
            [self.url_stub, self.url_source])
        try:
            self.db.commit()
            return True
        except:
            return False

    def log(self):
        # log request
        pass
