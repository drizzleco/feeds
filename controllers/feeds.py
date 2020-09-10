import datetime

from flask import jsonify, request
from flask_login import current_user
from slugify import slugify

from helpers import FEED_TYPES, token_or_session_authenticated
from models import Dashboard, Feed, db


@token_or_session_authenticated(user_scope=True)
def get_feeds():
    """Get Feeds
    Return all feeds belonging to user
    ---
    definitions:
        Feed:
            type: object
            properties:
                id:
                    type: integer
                    description: feed ID
                name:
                    type: string
                    description: feed name
                slug:
                    type: string
                    description: feed slug
                kind:
                    type: string
                    description: feed type
                    enum: ["text", "number", "boolean", "image"]
                created:
                    type: string
                    description: feed creation datetime
                owner:
                    type: string
                    description: username of feed's owner
                dashboard:
                    type: string
                    description: slug of dashboard feed is attached to
                data:
                    type: array
                    items:
                        $ref: '#/definitions/Data'
                    description: list of data posted to feed
    responses:
      200:
        description: A list the user's feeds
        schema:
            type: array
            items:
                $ref: '#/definitions/Feed'
    """
    return jsonify(feeds=[feed.to_dict() for feed in current_user.feeds]), 200


@token_or_session_authenticated(user_scope=True)
def get_feed(feed_slug):
    """Get a Feed
    Return info for one Feed
    ---
    parameters:
        - name: feed_slug
          in: path
          type: string
          required: true
    responses:
        200:
            description: The Feed object
            schema:
                $ref: '#/definitions/Feed'
        400:
            $ref: '#/definitions/Error'
    """
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if feed:
        return jsonify(feed.to_dict())
    else:
        return jsonify(error="Feed doesn't exist!"), 400


@token_or_session_authenticated(user_scope=True)
def new_feed():
    """New Feed
    Create a new Feed
    ---
    parameters:
        - name: name
          in: body
          schema:
            type: object
            required:
              - name
            properties:
                name:
                    type: string
                    description: name of new feed
                kind:
                    type: string
                    description: type for new feed
                    enum: ["text", "number", "boolean", "image"]
                dashboard:
                    type: string
                    description: slug of dashboard new feed belongs to
    responses:
        200:
            description: success
            schema:
                type: object
                properties:
                    message:
                        type: string
                    dashboard:
                        $ref: '#/definitions/Feed'
        400:
            $ref: '#/definitions/Error'
    """
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
    """Update Feed
    Update an existing Feed
    ---
    parameters:
        - name: feed_slug
          in: path
          type: string
          required: true
        - name: name
          in: body
          schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
                description: new name for feed
    responses:
        200:
            description: success
            schema:
                type: object
                properties:
                    message:
                        type: string
                    dashboard:
                        $ref: '#/definitions/Fashboard'
        400:
            $ref: '#/definitions/Error'
    """
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400

    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required."), 400
    if Feed.query.filter_by(slug=slugify(name), owner=current_user).first():
        return jsonify(error="A feed with that name already exists!"), 400
    feed.set_name(name)
    db.session.commit()
    return jsonify(message="Feed updated successfully!", feed=feed.to_dict())


@token_or_session_authenticated(user_scope=True)
def delete_feed(feed_slug):
    """Delete Feed
    Delete an existing Feed
    ---
    parameters:
        - name: feed_slug
          in: path
          type: string
          required: true
    responses:
        200:
            description: success
            schema:
                type: object
                properties:
                    message:
                        type: string
                        enum:
                            - Feed deleted!
        400:
            $ref: '#/definitions/Error'
    """
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user)
    if not feed.first():
        return jsonify(error="Feed doesn't exist!"), 400
    feed.delete()
    db.session.commit()
    return jsonify(message="Feed deleted!")
