import datetime

import validators
from flask import Flask, jsonify, render_template, request
from flask_login import current_user, login_user, logout_user

from helpers import token_or_session_authenticated
from models import User, db


def register():
    """Register a new user"""
    if not request.is_json:
        return jsonify(error="Missing JSON in request"), 400
    name = request.json.get("name", None)
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    confirm = request.json.get("confirm", None)
    if not name:
        return jsonify(error="Name is required."), 400
    if not username:
        return jsonify(error="Username is required."), 400
    if not email:
        return jsonify(error="Email is required."), 400
    if not password:
        return jsonify(error="Password is required."), 400
    if not confirm:
        return jsonify(error="Password confirmation is required."), 400
    if password != confirm:
        return jsonify(error="Passwords do not match"), 400
    if not validators.email(email):
        return jsonify(error="Invalid email"), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(error="User already exists."), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(error="Email already exists."), 400

    user = User(
        name=name,
        username=username,
        email=email,
        created=datetime.datetime.utcnow(),
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify(message="Successfully registered!", user=user.to_dict()), 200


def login():
    """Login a user"""
    if not request.is_json:
        return jsonify(error="Missing JSON in request"), 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    remember = request.json.get("remember", False)
    if not username:
        return jsonify(error="Username is required."), 400
    if not password:
        return jsonify(error="Password is required."), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        # try getting by email
        user = User.query.filter_by(email=username).first()

    if not user:
        return jsonify(error="User not found."), 401

    if not user.check_password(password):
        return jsonify(error="Invalid password."), 401

    login_user(user, remember=remember)
    return jsonify(message="Successfully logged in!", user=user.to_dict()), 200


def logout():
    """Log user out"""
    logout_user()
    return jsonify(message="Successfully logged out"), 200


@token_or_session_authenticated(user_scope=True)
def update_profile():
    """Update User Profile
    Update your user profile information.
    ---
    tags:
        - "Users"
    parameters:
        - name: user
          in: body
          schema:
            type: object
            properties:
              name:
                type: string
                description: new name
              username:
                type: string
                description: new username
              email:
                type: string
                description: new email
              password:
                type: string
                description: new password
              confirm:
                type: string
                description: confirm new password
    responses:
        200:
            description: Success
            schema:
                type: object
                properties:
                    message:
                        type: string
                    user:
                        $ref: '#/definitions/User'
        400:
            $ref: '#/responses/Error'
    """
    if not request.is_json:
        return jsonify(error="Missing JSON in request"), 400

    username = request.json.get("username", None)
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    confirm = request.json.get("confirm", None)
    if username:
        if (
            username != current_user.username
            and User.query.filter_by(username=username).first()
        ):
            return jsonify(error="Username taken"), 400
        current_user.username = username
    if name:
        current_user.name = name
    if email:
        if not validators.email(email):
            return jsonify(error="Invalid email"), 400
        if email != current_user.email and User.query.filter_by(email=email).first():
            return jsonify(error="Email taken"), 400
        current_user.email = email
    if password:
        if password != confirm:
            return jsonify(error="Passwords do not match"), 400
        current_user.set_password(password)
    db.session.commit()
    return jsonify(message="Successfully updated!", user=current_user.to_dict()), 200


@token_or_session_authenticated(user_scope=True)
def user_info():
    """Get current user info
    Return user info for token's owner
    ---
    tags:
        - "Users"
    responses:
        200:
            description: The User object
            schema:
                $ref: '#/definitions/User'
    """
    return jsonify(current_user.to_dict()), 200
