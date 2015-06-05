from functools import wraps
from flask import Response


def returns_text(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='text/plain; charset=utf-8')
    return decorated_function
