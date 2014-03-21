from flask import request, redirect, flash, url_for
from stub import Stub
from db import get_url_db


def redirect_stub(stub=None):
    db = get_url_db()
    db.execute('insert into requests (remote_addr, stub) values (?, ?)',
        [request.remote_addr, request.path])
    stub = Stub.get(stub)
    if stub:
        return redirect(stub.url_source)
    else:
        flash("Stub not found")
        return redirect(url_for("admin.stubs"))
