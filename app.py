from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_assets import Bundle, Environment
from flask_cors import CORS
from flask_login import LoginManager
from flasgger import Swagger

from config import Config
from models import User, db
from router import router


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # set up CORS
    CORS(app)
    # set up Sass
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle("scss/style.scss", filters="pyscss", output="css/style.css")
    assets.register("scss_all", scss)
    # set up db
    db.app = app
    db.init_app(app)
    # set up Flask Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("login_view"))

    # setup swagger
    swagger(app)

    # set up router
    router(app)

    return app


def swagger(app):
    """
    Configure app for Swagger
    """
    template = {
        "swagger": "2.0",
        "info": {
            "title": "feeds",
            "description": "# Welcome to the Feeds API",
            "contact": {
                "responsibleOrganization": "Drizzle",
            },
            "version": "1.0.0",
        },
        "schemes": ["http", "https"],
    }
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/",
    }
    Swagger(app, template=template, config=swagger_config)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
