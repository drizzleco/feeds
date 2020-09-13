import os
import random


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or "".join(
        [chr(random.randint(65, 92)) for _ in range(50)]
    )


swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "feeds",
        "description": "".join(open("swagger.md", "r").readlines()),
        "contact": {
            "responsibleOrganization": "Drizzle",
        },
        "version": "1.0.0",
    },
    "securityDefinitions": {
        "Token": {"in": "query", "name": "token", "type": "apiKey"},
    },
    "security": [{"Token": []}],
    "tags": [
        {
            "name": "Dashboards",
            "description": "Manage Dashboards (Token must have User Scope)",
        },
        {"name": "Feeds", "description": "Manage Feeds (Token must have User Scope)"},
        {
            "name": "Data Points",
            "description": "Manage Data (Token must have access to `feed_slug`)",
        },
        {"name": "Tokens", "description": "Manage Tokens (Token must have User Scope)"},
        {
            "name": "Users",
            "description": "Manage your profile (Token must have User Scope)",
        },
    ],
    "definitions": {
        "User": {
            "properties": {
                "id": {"description": "user's ID", "type": "string"},
                "name": {"description": "user's name", "type": "string"},
                "email": {"description": "user's email", "type": "string"},
                "username": {"description": "user's username", "type": "string"},
                "created": {
                    "description": "user's creation datetime",
                    "type": "string",
                },
                "dashboards": {
                    "description": "list of dashboards made by user",
                    "items": {"$ref": "#/definitions/Dashboard"},
                    "type": "array",
                },
                "feeds": {
                    "description": "list of feeds made by user",
                    "items": {"$ref": "#/definitions/Feed"},
                    "type": "array",
                },
            }
        },
        "Dashboard": {
            "properties": {
                "created": {
                    "description": "dashboard creation datetime",
                    "type": "string",
                },
                "feeds": {
                    "description": "list of feed attached to dashboard",
                    "items": {"$ref": "#/definitions/Feed"},
                    "type": "array",
                },
                "id": {"description": "dashboard ID", "type": "integer"},
                "name": {"description": "dashboard name", "type": "string"},
                "owner": {
                    "description": "username of dashboard's owner",
                    "type": "string",
                },
                "slug": {"description": "dashboard slug", "type": "string"},
            },
            "type": "object",
        },
        "Feed": {
            "properties": {
                "created": {"description": "feed creation datetime", "type": "string"},
                "dashboard": {
                    "description": "slug of dashboard feed is attached to",
                    "type": "string",
                },
                "data": {
                    "description": "list of data posted to feed",
                    "items": {"$ref": "#/definitions/Data"},
                    "type": "array",
                },
                "id": {"description": "feed ID", "type": "integer"},
                "kind": {
                    "description": "feed type",
                    "enum": ["text", "number", "boolean", "image"],
                    "type": "string",
                },
                "name": {"description": "feed name", "type": "string"},
                "owner": {"description": "username of feed's owner", "type": "string"},
                "slug": {"description": "feed slug", "type": "string"},
            },
            "type": "object",
        },
        "Data": {
            "properties": {
                "created": {"description": "data posted datetime", "type": "string"},
                "feed": {
                    "description": "slug of feed data belongs to",
                    "type": "string",
                },
                "id": {"description": "data ID", "type": "integer"},
                "value": {
                    "description": "data value",
                    "type": ["string", "bool", "number"],
                },
            },
            "type": "object",
        },
        "Token": {
            "properties": {
                "created": {"description": "token creation datetime", "type": "string"},
                "last_used": {
                    "description": "datetime token was last used",
                    "type": "string",
                },
                "allowed_feeds": {
                    "description": "list of feed slugs that token has access to",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "id": {"description": "token ID", "type": "integer"},
                "name": {
                    "description": "name of the token",
                    "type": "string",
                },
                "secret": {
                    "description": "token's secret",
                    "type": "string",
                },
                "owner": {
                    "description": "username of the owner of the token",
                    "type": "string",
                },
                "user_scope": {
                    "description": "true if token has user scope",
                    "type": "boolean",
                },
            },
            "type": "object",
        },
    },
    "responses": {
        "Error": {
            "description": "Error",
            "schema": {
                "properties": {
                    "error": {"description": "error message", "type": "string"}
                },
                "type": "object",
            },
        },
    },
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
