from flask import request, redirect, flash, url_for
from stub import Stub


def redirect_stub(stub=None):
    stub = Stub.get(stub)
    if stub:
        stub.log(request.remote_addr)
        return redirect(stub.url_source)
    else:
        flash("Stub not found")
        return redirect(url_for("index"))
