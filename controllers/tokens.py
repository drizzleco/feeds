from flask import jsonify
from flask_login import current_user

from helpers import token_or_session_authenticated


@token_or_session_authenticated(user_scope=True)
def get_tokens():
    return jsonify(tokens=[token.to_dict() for token in current_user.tokens]), 200
