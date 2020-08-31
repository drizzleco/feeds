from functools import wraps
from typing import List, Dict

from flask import redirect, request
from flask_login import current_user

import models


def token_or_session_authenticated(user_scope):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if request.json:
                token = request.json.get("token", None)
            elif request.args:
                # try query string
                token = request.args.get("token", None)
            elif current_user.is_anonymous:
                return "Oops! you forgot to supply a token!", 401
            # check token
            if token:
                token_obj = models.Token.query.filter_by(secret=token).first()
                if not token_obj and current_user.is_anonymous:
                    return "Oops! Invalid token!", 401
                if user_scope and current_user.is_anonymous:
                    if not token_obj.user_scope():
                        return "Oops! Token does not have user scope!", 401
            return f(*args, **kwargs)

        return wrapper

    return decorator


def slugify(name: str):
    return name.lower().replace(" ", "-")


def filter_params(
    params: Dict,
    allowed: List[str],
):
    return {k: v for k, v in params.items() if k in allowed}
