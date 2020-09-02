from client import client
from test_register import register
from test_dashboards import create_dashboard


def get_feed(client, slug):
    return client.get("/api/feeds/" + slug)


def get_feeds(client):
    return client.get("/api/feeds")


def create_feed(client, name="", kind="", dashboard=""):
    return client.post(
        "/api/feeds/new",
        json={
            "name": name,
            "kind": kind,
            "dashboard": dashboard,
        },
    )


def update_feed(client, slug, name=""):
    return client.put(
        "/api/feeds/" + slug,
        json={"name": name},
    )


def delete_feed(client, slug):
    return client.delete("/api/feeds/" + slug)


def test_get_feeds_returns_empty(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = get_feeds(client)
    assert not resp.json


def test_get_feeds_returns_feeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = get_feeds(client)
    result = {
        "dashboard": "test-dash",
        "data": [],
        "id": 1,
        "kind": "text",
        "name": "test feed",
        "owner": "test",
        "slug": "test-feed",
    }
    assert any([(k, v) in result.items() for (k, v) in resp.json[0].items()])


def test_get_feed_doesnt_exist_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = get_feed(client, "blah")
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_create_feed_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    resp = create_feed(client, "test feed", "text", "test-dash")
    assert resp.json.get("message") == "Feed created successfully!"


def test_create_duplicate_feed_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test", "image", "test-dash")
    resp = create_feed(client, "test", "boolean", "test-dash")
    assert resp.json.get("error") == "A feed with that name already exists!"


def test_create_feed_no_name_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_feed(client)
    assert resp.json.get("error") == "Name is required."


def test_create_feed_no_kind_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_feed(client, "test")
    assert resp.json.get("error") == "Kind is required."


def test_create_feed_no_dashboard_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_feed(client, "test", "text")
    assert resp.json.get("error") == "Dashboard slug is required."


def test_create_feed_nonexistent_dash_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_feed(client, "test", "text", "blah")
    assert resp.json.get("error") == "Dashboard doesn't exist!"


def test_update_feed_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    update_feed(client, "test-feed", "tester")
    resp = get_feed(client, "tester")
    assert resp.json.get("slug") == "tester"


def test_update_nonexistent_feed_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = update_feed(client, "blah", "test")
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_update_feed_no_name_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = update_feed(client, "test-feed")
    assert resp.json.get("error") == "Name is required."


def test_delete_feed_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = delete_feed(client, "test-feed")
    assert resp.json.get("message") == "Feed deleted!"


def test_delete_nonexistent_feed_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = delete_feed(client, "blah")
    assert resp.json.get("error") == "Feed doesn't exist!"
