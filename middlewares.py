from functools import wraps
from flask import session
from uuid import uuid4


def session_manager(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get('user', None):
            session['user'] = str(uuid4())[:4]

        return function(*args, **kwargs)

    return wrapper
