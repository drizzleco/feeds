from client import client
from test_register import register
from test_dashboards import create_dashboard
from test_feeds import create_feed
from test_data import create_data


def get_tokens(client):
    return client.get("/api/tokens")


def create_token(client, name="", feeds="", user_scope=""):
    return client.post(
        "/api/tokens/new", json={"name": name, "feeds": feeds, "user_scope": user_scope}
    )


def delete_token(client, token_id):
    return client.delete(f"/api/tokens/{token_id}")


def test_get_tokens_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    create_token(client, "test token", "test-feed", False)
    resp = get_tokens(client)
    result = {
        "allowed_feeds": ["test-feed"],
        "id": 1,
        "last_used": None,
        "name": "test token",
        "owner": "test",
        "user_scope": False,
    }
    assert any(
        [(k, v) in result.items() for (k, v) in resp.json.get("tokens")[0].items()]
    )


def test_create_token_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = create_token(client, "test token", "test-feed", False)
    assert resp.json.get("message") == "Token created!"


def test_create_token_name_missing_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = create_token(client)
    assert resp.json.get("error") == "Name is required"


def test_create_token_nonexisten_feed_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_token(client, "test", "blah")
    assert resp.json.get("error") == "blah doesn't exist!"


def test_create_token_user_scope_not_boolean_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = create_token(client, "test token", "test-feed")
    assert resp.json.get("error") == "user_scope must be a boolean!"


def test_delete_token_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    create_token(client, "test token", "test-feed", False)
    resp = delete_token(client, 1)
    assert resp.json.get("message") == "Token deleted!"


def test_delete_nonexistent_token_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = delete_token(client, 1)
    assert resp.json.get("error") == "Token doesn't exist!"


def test_invalid_token_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_dashboard(client, "test dash", token="invalid token")
    assert resp.json.get("error") == "Oops! Invalid token!"


def test_user_scope_token_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    token = create_token(client, "token", "test-feed", user_scope=True).json["token"][
        "secret"
    ]
    resp = create_dashboard(client, "dash", token=token)
    assert resp.json.get("message") == "Dashboard created successfully!"


def test_non_user_scope_token_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    token = create_token(client, "token", "test-feed", user_scope=False).json["token"][
        "secret"
    ]
    resp = create_dashboard(client, "test dash", token=token)
    assert resp.json.get("error") == "Oops! Token does not have user scope!"


def test_feed_scope_token_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    token = create_token(client, "token", "test-feed", user_scope=False).json["token"][
        "secret"
    ]
    resp = create_data(client, "test-feed", "test", token=token)
    assert resp.json.get("message") == "Data posted!"


def test_non_feed_scope_token_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    create_feed(client, "another feed", "text", "test-dash")
    token = create_token(client, "token", "test-feed", user_scope=False).json["token"][
        "secret"
    ]
    resp = create_data(client, "another-feed", "test", token=token)
    assert resp.json.get("error") == "Oops! Token not authorized to access this feed."


def test_no_token_fails(client):
    resp = create_dashboard(client, "test dash")
    assert resp.json.get("error") == "Oops! you forgot to supply a token!"
