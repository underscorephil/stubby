import string
from random import choice
from flask import flash
from stubby.utils.db import get_url_db, get_stats_db

from pprint import pprint as pp

class Stub():
    def __init__(self, url_source=None, url_stub=None):
        self.url_source = url_source
        self.url_stub = url_stub or self._generate_stub()
        self.db = get_url_db()

    def _generate_stub(self, length=6, uppercase=True, lowercase=True,
                       digits=True):
        pool = ''
        if uppercase:
            pool += string.uppercase
        if lowercase:
            pool += string.lowercase
        if digits:
            pool += string.digits

        if length < 1:
            length = 1
        return ''.join([choice(pool) for x in xrange(length)])

    def save(self):
        pp(self.url_stub)
        self.db.execute(
            'insert into stubs (url_source, url_stub) values (?, ?)',
            [self.url_source, self.url_stub])
        try:
            self.db.commit()
            flash("Stub %s Added" % self.url_stub)
            return True
        except:
            flash("Stub creation failed")
            return False

    @classmethod
    def get(cls, url_stub):
        stub = None
        db = get_url_db()

        cur = db.execute(
            'select url_source, url_stub from stubs where url_stub=?',
            [url_stub])
        res = cur.fetchone()

        if res:
            stub = cls(res[0], res[1])
        return stub

    def delete(self):
        pp(self.url_stub)
        self.db.execute('delete from stubs where url_stub=?',
            [self.url_stub])
        try:
            self.db.commit()
            # commit() returns true check if the delete occured(effected rules)
            flash("Stub %s deleted" % self.url_stub)
            return True
        except:
            flash("Stub %s not deleted" % self.url_stub)
            return False

    def log(self, address):
        db = get_stats_db()
        db.execute('insert into requests (remote_addr, stub) values (?, ?)',
        [address, self.url_stub])
