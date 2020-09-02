from controllers.sessions import *
from controllers.dashboards import *
from controllers.tokens import *
from config import api_path


def router(app):
    # user auth routes
    app.add_url_rule("/register", view_func=register, methods=["POST"])
    app.add_url_rule("/login", view_func=login, methods=["POST"])
    app.add_url_rule("/logout", view_func=logout, methods=["DELETE"])
    # dashboard routes
    app.add_url_rule(
        api_path + "/dashboards",
        view_func=get_dashboards,
        methods=["GET"],
    )
    app.add_url_rule(
        api_path + "/dashboards/<dashboard_slug>",
        view_func=get_dashboard,
        methods=["GET"],
    )
    app.add_url_rule(
        api_path + "/dashboards/<dashboard_slug>",
        view_func=update_dashboard,
        methods=["PUT"],
    )
    app.add_url_rule(
        api_path + "/dashboards/new",
        view_func=new_dashboard,
        methods=["POST"],
    )
    app.add_url_rule(
        api_path + "/dashboards/<dashboard_slug>",
        view_func=delete_dashboard,
        methods=["DELETE"],
    )
    # token routes
    app.add_url_rule(
        api_path + "/tokens",
        view_func=get_tokens,
        methods=["GET"],
    )
