import datetime

from flask import jsonify, request
from flask_login import current_user
from slugify import slugify

from helpers import token_or_session_authenticated, FEED_TYPES
from models import db, Feed, Dashboard


@token_or_session_authenticated(user_scope=True)
def get_feeds():
    return jsonify([feed.to_dict() for feed in current_user.feeds]), 200


@token_or_session_authenticated(user_scope=True)
def get_feed(feed_slug):
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if feed:
        return jsonify(feed.to_dict())
    else:
        return jsonify(error="Feed doesn't exist!"), 400


@token_or_session_authenticated(user_scope=True)
def new_feed():
    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required."), 400
    kind = request.json.get("kind", None)
    if not kind:
        return jsonify(error="Kind is required."), 400
    if kind not in FEED_TYPES:
        return jsonify(error="Kind must be one of these: " + FEED_TYPES), 400
    dashboard_slug = request.json.get("dashboard", None)
    if not dashboard_slug:
        return jsonify(error="Dashboard slug is required."), 400
    dashboard = Dashboard.query.filter_by(
        slug=dashboard_slug, owner=current_user
    ).first()
    if not dashboard:
        return jsonify(error="Dashboard doesn't exist!"), 400

    feed = Feed.query.filter_by(slug=slugify(name), owner=current_user).first()
    if feed:
        return jsonify(error="A feed with that name already exists!"), 400
    feed = Feed(
        created=datetime.datetime.utcnow(),
        owner=current_user,
        dashboard=dashboard,
        kind=kind,
    )
    feed.set_name(name)
    db.session.add(feed)
    db.session.commit()
    return (
        jsonify(message="Feed created successfully!", feed=feed.to_dict()),
        200,
    )


@token_or_session_authenticated(user_scope=True)
def update_feed(feed_slug):
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400

    name = request.json.get("name", None)
    if not name:
        return jsonify(error="'Name' is required."), 400

    feed.set_name(name)
    db.session.commit()
    return jsonify(message="Feed updated successfully!", feed=feed.to_dict())


@token_or_session_authenticated(user_scope=True)
def delete_feed(feed_slug):
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user)
    if not feed.first():
        return jsonify(error="Feed doesn't exist!"), 400
    feed.delete()
    db.session.commit()
    return jsonify(message="Feed deleted!")