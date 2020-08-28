import datetime

from flask import Flask, jsonify, render_template, request
from flask_login import login_user, logout_user, current_user

from models import User, db


def register():
    """Register a new user"""
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    confirm = request.json.get("confirm", None)
    if not username:
        return jsonify({"message": "Username is required."}), 400
    if not email:
        return jsonify({"message": "Email is required."}), 400
    if not password:
        return jsonify({"message": "Password is required."}), 400
    if not confirm:
        return jsonify({"message": "Password confirmation is required."}), 400
    if password != confirm:
        return jsonify({"message": "Passwords do not match"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "User already exists."}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already exists."}), 400

    user = User(
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
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    remember = request.json.get("remember", False)
    if not username:
        return jsonify({"message": "Username is required."}), 400
    if not password:
        return jsonify({"message": "Password is required."}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        # try getting by email
        user = User.query.filter_by(email=username).first()

    if not user:
        return jsonify({"message": "User not found."}), 401

    if not user.check_password(password):
        return jsonify({"message": "Invalid password."}), 401

    login_user(user, remember=remember)
    return jsonify(message="Successfully logged in!", user=user.to_dict()), 200


def logout():
    """Log user out"""
    logout_user()
    return jsonify(message="Successfully logged out"), 200
