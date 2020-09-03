from flask import render_template, redirect
from flask_login import current_user


def home_view():
    return render_template("index.html")


def login_view():
    if not current_user.is_anonymous:
        return redirect("/dashboard")
    return render_template("login.html")


def register_view():
    if not current_user.is_anonymous:
        return redirect("/dashboard")
    return render_template("register.html")
