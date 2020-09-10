import datetime
from functools import wraps

from flask import jsonify, redirect, request
from flask_login import current_user, login_user, logout_user

import models

FEED_TYPES = ["text", "number", "boolean", "image"]


def token_or_session_authenticated(user_scope=False, feed_scope=False):
    """
    Functions decorated with this are authenticated with
    either a valid token or a current session
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if request.json:
                token = request.json.get("token", None)
            elif request.args:
                # try query string
                token = request.args.get("token", None)
            # user not logged in and token supplied
            if token:
                # check token
                token_obj = models.Token.query.filter_by(secret=token).first()
                if not token_obj:
                    return jsonify(error="Oops! Invalid token!"), 401
                token_owner = token_obj.owner
                if user_scope and not token_obj.user_scope:
                    return (
                        jsonify(error="Oops! Token does not have user scope!"),
                        401,
                    )
                if feed_scope:
                    feed = models.Feed.query.filter_by(
                        slug=kwargs.get("feed_slug"), owner=token_owner, token=token_obj
                    ).first()
                    if not feed:
                        return (
                            jsonify(error="Oops! Token not authorized to access this feed."),
                            401,
                        )
                token_obj.last_used = datetime.datetime.utcnow()
                models.db.session.add(token_obj)
                models.db.session.commit()
                login_user(token_owner)  # login user so that current_user proxy works
            elif not current_user.is_anonymous:
                # user is logged in
                pass
            else:
                return jsonify(error="Oops! you forgot to supply a token!"), 401
            func = f(*args, **kwargs)
            if token:
                logout_user()  # logout user after a token request
            return func

        return wrapper

    return decorator
