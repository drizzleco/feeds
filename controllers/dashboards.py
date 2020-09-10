import datetime

from flask import jsonify, request
from flask_login import current_user
from slugify import slugify

from helpers import token_or_session_authenticated
from models import Dashboard, db


@token_or_session_authenticated(user_scope=True)
def get_dashboards():
    """Get Dasboards
    Return all dashboards belonging to user
    ---
    definitions:
        Dashboard:
            type: object
            properties:
                id:
                    type: integer
                    description: dashboard ID
                name:
                    type: string
                    description: dashboard name
                slug:
                    type: string
                    description: dashboard slug
                created:
                    type: string
                    description: dashboard creation datetime
                owner:
                    type: string
                    description: username of dashboard's owner
                feeds:
                    type: array
                    items:
                        $ref: '#/definitions/Feed'
                    description: list of feed attached to dashboard
    responses:
      200:
        description: A list the user's dashboards
        schema:
            type: array
            items:
                $ref: '#/definitions/Dashboard'
    """
    return (
        jsonify(
            dashboards=[dashboard.to_dict() for dashboard in current_user.dashboards]
        ),
        200,
    )


@token_or_session_authenticated(user_scope=True)
def get_dashboard(dashboard_slug):
    """Get a Dashboard
    Return info for one Dashboard
    ---
    definitions:
        Error:
            description: error
            schema:
                type: object
                properties:
                    error:
                        type: string
                        description: error message
    parameters:
        - name: dashboard_slug
          in: path
          type: string
          required: true
    responses:
        200:
            description: The Dashboard object
            schema:
                $ref: '#/definitions/Dashboard'
        400:
            $ref: '#/definitions/Error'
    """
    dashboard = Dashboard.query.filter_by(
        slug=dashboard_slug, owner=current_user
    ).first()
    if dashboard:
        return jsonify(dashboard.to_dict()), 200
    else:
        return jsonify(error="Dashboard doesn't exist!"), 400


@token_or_session_authenticated(user_scope=True)
def new_dashboard():
    """New Dashboard
    Create a new Dashboard
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
                description: name of new dashboard
    responses:
        200:
            description: success
            schema:
                type: object
                properties:
                    message:
                        type: string
                    dashboard:
                        $ref: '#/definitions/Dashboard'
        400:
            $ref: '#/definitions/Error'
    """
    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required."), 400
    dashboard = Dashboard.query.filter_by(
        slug=slugify(name), owner=current_user
    ).first()
    if dashboard:
        return jsonify(error="A dashboard with that name already exists!"), 400
    dashboard = Dashboard(
        created=datetime.datetime.utcnow(),
        owner=current_user,
    )
    dashboard.set_name(name)
    db.session.add(dashboard)
    db.session.commit()
    return (
        jsonify(
            message="Dashboard created successfully!", dashboard=dashboard.to_dict()
        ),
        200,
    )


@token_or_session_authenticated(user_scope=True)
def update_dashboard(dashboard_slug):
    """Update Dashboard
    Update an existing Dashboard
    ---
    parameters:
        - name: dashboard_slug
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
                description: new name for dashboard
    responses:
        200:
            description: success
            schema:
                type: object
                properties:
                    message:
                        type: string
                    dashboard:
                        $ref: '#/definitions/Dashboard'
        400:
            $ref: '#/definitions/Error'
    """
    dashboard = Dashboard.query.filter_by(
        slug=dashboard_slug, owner=current_user
    ).first()
    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required."), 400
    if Dashboard.query.filter_by(slug=slugify(name), owner=current_user).first():
        return jsonify(error="A dashboard with that name already exists!"), 400
    if dashboard:
        dashboard.set_name(name)
        db.session.commit()
        return jsonify(
            message="Dashboard updated successfully!", dashboard=dashboard.to_dict()
        )
    else:
        return jsonify(error="Dashboard doesn't exist!"), 400


@token_or_session_authenticated(user_scope=True)
def delete_dashboard(dashboard_slug):
    """Delete Dashboard
    Delete an existing Dashboard
    ---
    parameters:
        - name: dashboard_slug
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
                            - Dashboard deleted!
        400:
            $ref: '#/definitions/Error'
    """
    dashboard = Dashboard.query.filter_by(slug=dashboard_slug, owner=current_user)
    if not dashboard.first():
        return jsonify(error="Dashboard doesn't exist!"), 400
    dashboard.delete()
    db.session.commit()
    return jsonify(message="Dashboard deleted!")
