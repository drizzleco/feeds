import datetime

from flask import jsonify, request
from flask_login import current_user
from slugify import slugify

from helpers import token_or_session_authenticated
from models import Dashboard, db


@token_or_session_authenticated(user_scope=True)
def get_dashboards():
    return (
        jsonify(dashboards=[dashboard.to_dict() for dashboard in current_user.dashboards]),
        200,
    )


@token_or_session_authenticated(user_scope=True)
def get_dashboard(dashboard_slug):
    dashboard = Dashboard.query.filter_by(slug=dashboard_slug, owner=current_user).first()
    if dashboard:
        return jsonify(dashboard.to_dict())
    else:
        return jsonify(error="Dashboard doesn't exist!"), 400


@token_or_session_authenticated(user_scope=True)
def new_dashboard():
    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required."), 400
    dashboard = Dashboard.query.filter_by(slug=slugify(name), owner=current_user).first()
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
        jsonify(message="Dashboard created successfully!", dashboard=dashboard.to_dict()),
        200,
    )


@token_or_session_authenticated(user_scope=True)
def update_dashboard(dashboard_slug):
    dashboard = Dashboard.query.filter_by(slug=dashboard_slug, owner=current_user).first()
    name = request.json.get("name", None)
    if not name:
        return jsonify(error="Name is required."), 400
    if Dashboard.query.filter_by(slug=slugify(name), owner=current_user).first():
        return jsonify(error="A dashboard with that name already exists!"), 400
    if dashboard:
        dashboard.set_name(name)
        db.session.commit()
        return jsonify(message="Dashboard updated successfully!", dashboard=dashboard.to_dict())
    else:
        return jsonify(error="Dashboard doesn't exist!"), 400


@token_or_session_authenticated(user_scope=True)
def delete_dashboard(dashboard_slug):
    dashboard = Dashboard.query.filter_by(slug=dashboard_slug, owner=current_user)
    if not dashboard.first():
        return jsonify(error="Dashboard doesn't exist!"), 400
    dashboard.delete()
    db.session.commit()
    return jsonify(message="Dashboard deleted!")
