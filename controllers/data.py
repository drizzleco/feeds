import datetime

import validators
from flask import jsonify, request
from flask_login import current_user
from sqlalchemy import desc

from helpers import is_a_number, token_or_session_authenticated
from models import Data, Feed, db


@token_or_session_authenticated(feed_scope=True)
def create_data(feed_slug):
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400
    value = request.json.get("value", None)
    if not value:
        return jsonify(error="Value is required."), 400
    if (
        (feed.kind == "number" and not is_a_number(value))
        or (feed.kind == "boolean" and value.lower() not in ["true", "false"])
        or (feed.kind == "image" and not validators.url(value))
    ):
        return (
            jsonify(
                error=f"Invalid value. Type '{feed.kind}' was expected but got '{value}'."
            ),
            400,
        )

    data = Data(value=value, created=datetime.datetime.utcnow(), feed=feed)
    db.session.add(data)
    db.session.commit()
    return jsonify(message="Data posted!", data=data.to_dict()), 200


@token_or_session_authenticated(feed_scope=True)
def get_data(feed_slug):
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400
    last = request.args.get("last", "10")
    if not last.isnumeric():
        return jsonify(error="Last must be an integer!"), 400
    data = sorted(feed.data, key=lambda data: data.created, reverse=True)[: int(last)]
    return jsonify(data=[data.to_dict() for data in data])


@token_or_session_authenticated(feed_scope=True)
def delete_data(feed_slug, data_id):
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400
    data = Data.query.filter_by(id=data_id, feed=feed)
    if not data.first():
        return jsonify(error="Data point doesn't exist!"), 400
    data.delete()
    db.session.commit()
    return jsonify(message="Data point deleted!"), 200
