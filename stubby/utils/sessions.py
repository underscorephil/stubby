
from flask.ext.login import LoginManager

_login_manager = LoginManager()


def get_session_manager():
    # can't use lazy_load here because g requires a request context
    # and these are setup before that
    return _login_manager
