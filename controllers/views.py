from flask import render_template, redirect, url_for
from flask_login import current_user


def home_view():
    return render_template("index.html")


def login_view():
    if not current_user.is_anonymous:
        return redirect(url_for("user_homepage_view"))
    return render_template("login.html")


def register_view():
    if not current_user.is_anonymous:
        return redirect(url_for("user_homepage_view"))
    return render_template("register.html")


def user_homepage_view():
    if current_user.is_anonymous:
        return redirect(url_for("login_view"))
    return render_template("home.html")
