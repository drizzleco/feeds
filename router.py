from controllers.sessions import *
from controllers.dashboards import *
from controllers.tokens import *
from config import api_path


def router(app):
    # user auth routes
    app.add_url_rule("/register", "register", view_func=register, methods=["POST"])
    app.add_url_rule("/login", "login", view_func=login, methods=["POST"])
    app.add_url_rule("/logout", "logout", view_func=logout, methods=["DELETE"])
    # dashboard routes
    app.add_url_rule(
        api_path + "/dashboards",
        "get_dashboards",
        view_func=get_dashboards,
        methods=["GET"],
    )
    # token routes
    app.add_url_rule(
        api_path + "/tokens",
        "get_tokens",
        view_func=get_tokens,
        methods=["GET"],
    )
