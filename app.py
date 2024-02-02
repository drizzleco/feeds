from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_assets import Bundle, Environment
from flask_cors import CORS
from flask_login import LoginManager
from flasgger import Swagger

from config import Config, swagger_config, swagger_template
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
    Swagger(app, template=swagger_template, config=swagger_config)

    # set up router
    router(app)

    return app


app = create_app()
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
