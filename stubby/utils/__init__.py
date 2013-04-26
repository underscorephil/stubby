from functools import wraps
from flask import g


def lazy_load(attr_name):
    """ lazy loads attributes onto flask.g and treats flask.g as a cache."""
    attr_name = str(attr_name)

    def inner_wrapper(f):
        def wrapper(*args, **kwargs):
            if not hasattr(g, attr_name) or not getattr(g, attr_name):
                setattr(g, attr_name, f(*args, **kwargs))
            return getattr(g, attr_name)
        return wraps(f)(wrapper)
    return inner_wrapper
