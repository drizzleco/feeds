from flask import jsonify
from flask_login import current_user
from helpers import token_or_session_authenticated


@token_or_session_authenticated(user_scope=True)
def get_dashboards():
    return jsonify([dashboard.to_dict() for dashboard in current_user.dashboards]), 200
