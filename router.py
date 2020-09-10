from controllers.dashboards import *
from controllers.data import *
from controllers.feeds import *
from controllers.sessions import *
from controllers.tokens import *
from controllers.views import *

api_path = "/api"

# fmt: off
def router(app):
    # VIEW ROUTES
    app.add_url_rule("/", endpoint='home_view', view_func=home_view, methods=["GET"])
    app.add_url_rule('/login', endpoint='login_view', view_func=login_view, methods=['GET'])
    app.add_url_rule('/register', endpoint='register_view', view_func=register_view, methods=['GET'])
    app.add_url_rule('/home', endpoint='user_homepage_view', view_func=user_homepage_view, methods=['GET'])
    app.add_url_rule('/dashboard/<dashboard_slug>', endpoint='dashboard_view', view_func=dashboard_view, methods=['GET'])
    app.add_url_rule('/feed/<feed_slug>', endpoint='feed_view', view_func=feed_view, methods=['GET'])
    # API ROUTES
    # user routes
    app.add_url_rule("/register", view_func=register, methods=["POST"])
    app.add_url_rule("/login", view_func=login, methods=["POST"])
    app.add_url_rule("/logout", view_func=logout, methods=["DELETE"])
    app.add_url_rule("/me", view_func=update_profile, methods=["PUT"])
    # dashboard routes
    app.add_url_rule(api_path + "/dashboards", view_func=get_dashboards,methods=["GET"])
    app.add_url_rule(api_path + "/dashboards/<dashboard_slug>", view_func=get_dashboard, methods=["GET"],)
    app.add_url_rule(api_path + "/dashboards/<dashboard_slug>", view_func=update_dashboard, methods=["PUT"])
    app.add_url_rule(api_path + "/dashboards/new", view_func=new_dashboard, methods=["POST"])
    app.add_url_rule(api_path + "/dashboards/<dashboard_slug>", view_func=delete_dashboard, methods=["DELETE"])
    # feed routes
    app.add_url_rule(api_path + "/feeds", view_func=get_feeds,methods=["GET"])
    app.add_url_rule(api_path + "/feeds/<feed_slug>", view_func=get_feed, methods=["GET"],)
    app.add_url_rule(api_path + "/feeds/<feed_slug>", view_func=update_feed, methods=["PUT"])
    app.add_url_rule(api_path + "/feeds/new", view_func=new_feed, methods=["POST"])
    app.add_url_rule(api_path + "/feeds/<feed_slug>", view_func=delete_feed, methods=["DELETE"])
    # data routes
    app.add_url_rule(api_path + "/feeds/<feed_slug>/data", view_func=create_data, methods=["POST"])
    app.add_url_rule(api_path + "/feeds/<feed_slug>/data", view_func=get_data, methods=["GET"])
    app.add_url_rule(api_path + "/feeds/<feed_slug>/data/<data_id>", view_func=delete_data, methods=["DELETE"])
    # token routes
    app.add_url_rule(api_path + "/tokens", view_func=get_tokens, methods=["GET"])
    app.add_url_rule(api_path + "/tokens/new", view_func=create_token, methods=["POST"])
    app.add_url_rule(api_path + "/tokens/<token_id>", view_func=delete_token, methods=["DELETE"])
# fmt: on
