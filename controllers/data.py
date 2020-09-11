import datetime

import validators
from flask import jsonify, request
from flask_login import current_user
from sqlalchemy import desc

from helpers import token_or_session_authenticated
from models import Data, Feed, db


@token_or_session_authenticated(feed_scope=True)
def create_data(feed_slug):
    """Post Data
    Post a data point to a feed
    ---
    tags:
        - "Data Points"
    parameters:
        - name: feed_slug
          in: path
          type: string
          required: true
        - name: value
          in: body
          schema:
            type: object
            required:
              - value
            properties:
              value:
                type: stringboolnumber
                description: value of data to post. must be the same data type as feed kind
    responses:
        200:
            description: Success
            schema:
                type: object
                properties:
                    message:
                        type: string
                    data:
                        $ref: '#/definitions/Data'
        400:
            $ref: '#/responses/Error'
    """
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400
    value = request.json.get("value", None)
    if value is None:
        return jsonify(error="Value is required."), 400
    if (
        (
            feed.kind == "number"
            and not (isinstance(value, int) or isinstance(value, float))
        )
        or (feed.kind == "boolean" and not isinstance(value, bool))
        or (feed.kind == "image" and not validators.url(value))
    ):
        return (
            jsonify(
                error=f"Invalid value. Type '{feed.kind}' was expected but got '{value}'."
            ),
            400,
        )

    data = Data(value=str(value), created=datetime.datetime.utcnow(), feed=feed)
    db.session.add(data)
    db.session.commit()
    return jsonify(message="Data posted!", data=data.to_dict()), 200


@token_or_session_authenticated(feed_scope=True)
def get_data(feed_slug):
    """Get Data
    Get data for a Feed
    ---
    tags:
        - "Data Points"
    parameters:
        - name: feed_slug
          in: path
          type: string
          required: true
        - name: limit
          in: query
          type: integer
          description: total number of results to return per page. Default is 10
        - name: page
          in: query
          type: integer
          description: page number to retreive. Default is 1
        - name: order
          in: query
          type: string
          description: order to retrieve data in sorted by the data point's posted datetime. Must be either 'asc' or 'desc'. Default is 'desc'
    responses:
        200:
            description: Data from feed
            schema:
                type: object
                properties:
                    data:
                        type: array
                        items:
                            $ref: '#/definitions/Data'
                    total:
                        type: integer
                        description: total data points on Feed
        400:
            $ref: '#/responses/Error'
    """
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400
    limit = request.args.get("limit", "10")
    page = request.args.get("page", "1")
    order = request.args.get("order", "desc")
    if not limit.isnumeric():
        return jsonify(error="Limit must be an integer!"), 400
    if not page.isnumeric():
        return jsonify(error="Page must be an integer!"), 400
    if order not in ["asc", "desc"]:
        return jsonify(error="Order must be either 'asc' or 'desc'"), 400
    data_query = Data.query.filter_by(feed=feed)
    data = (
        data_query.order_by(getattr(Data.created, order)())
        .paginate(int(page), int(limit), False)
        .items
    )
    total = data_query.count()
    return jsonify(data=[data.to_dict() for data in data], total=total)


@token_or_session_authenticated(feed_scope=True)
def delete_data(feed_slug, data_id):
    """Delete Data
    Delete a data point from feed
    ---
    tags:
        - "Data Points"
    parameters:
        - name: feed_slug
          in: path
          type: string
          required: true
        - name: data_id
          in: path
          type: integer
          required: true
          description: ID of Data Point to delete
    responses:
        200:
            description: Success
            schema:
                type: object
                properties:
                    message:
                        type: string
                        enum:
                            - Data point deleted!
        400:
            $ref: '#/responses/Error'
    """
    feed = Feed.query.filter_by(slug=feed_slug, owner=current_user).first()
    if not feed:
        return jsonify(error="Feed doesn't exist!"), 400
    data = Data.query.filter_by(id=data_id, feed=feed)
    if not data.first():
        return jsonify(error="Data point doesn't exist!"), 400
    data.delete()
    db.session.commit()
    return jsonify(message="Data point deleted!"), 200
