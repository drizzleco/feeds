from functools import wraps
from flask import request, redirect
from flask_login import current_user
from models import Token


def token_or_session_authenticated(user_scope):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.json:
                token = request.json.get("token", None)
            elif request.args:
                # try query string
                token = request.args.get("token", None)
            elif current_user.is_anonymous:
                return "Oops! you forgot to supply a token!", 401
            # check token
            token = Token.query.filter_by(secret=token).first()
            if not token and current_user.is_anonymous:
                return "Oops! Invalid token!", 401
            if user_scope and current_user.is_anonymous:
                if not token.user_scope():
                    return "Oops! Token does not have user scope!", 401
            return f(*args, **kwargs)

        return wrapper

    return decorator
