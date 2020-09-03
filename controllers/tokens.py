import datetime

from flask import jsonify, request
from flask_login import current_user

from helpers import token_or_session_authenticated
from models import db, Token, Feed


@token_or_session_authenticated(user_scope=True)
def get_tokens():
    return jsonify(tokens=[token.to_dict() for token in current_user.tokens]), 200


@token_or_session_authenticated(user_scope=True)
def create_token():
    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required"), 400
    feeds = request.json.get("feeds", None)
    feed_slugs = []
    feed_objs = []
    if isinstance(feeds, str):
        feed_slugs.append(feeds)
    elif isinstance(feeds, list):
        feed_slugs.extend(feeds)
    for slug in feed_slugs:
        feed = Feed.query.filter_by(slug=slug, owner=current_user).first()
        if not feed:
            return jsonify(error=f"{slug} doesn't exist!"), 400
        feed_objs.append(feed)
    user_scope = request.json.get("user_scope", False)
    if not isinstance(user_scope, bool):
        return jsonify(error="user_scope must be a boolean!"), 400

    token = Token(
        name=name,
        allowed_feeds=feed_objs,
        user_scope=user_scope,
        created=datetime.datetime.utcnow(),
        owner=current_user,
    )
    token.generate_secret()
    db.session.add(token)
    db.session.commit()
    return jsonify(message="Token created!", token=token.to_dict()), 200


@token_or_session_authenticated(user_scope=True)
def delete_token(token_id):
    token = Token.query.filter_by(id=token_id, owner=current_user)
    if not token.first():
        return jsonify(error="Token doesn't exist!"), 400
    token.delete()
    db.session.commit()
    return jsonify(message="Token deleted!"), 200
