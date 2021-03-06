from flask import redirect, render_template, url_for
from flask_login import current_user, login_required


def home_view():
    return render_template("index.html")


def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("user_homepage_view"))
    return render_template("login.html")


def register_view():
    if current_user.is_authenticated:
        return redirect(url_for("user_homepage_view"))
    return render_template("register.html")


@login_required
def user_homepage_view():
    return render_template("home.html")


@login_required
def dashboard_view(dashboard_slug):
    return render_template("dashboard.html", dashboard_slug=dashboard_slug)


@login_required
def feed_view(feed_slug):
    return render_template("feed.html", feed_slug=feed_slug)


@login_required
def devices_view():
    return render_template("devices.html")


@login_required
def profile_view():
    return render_template("profile.html")
