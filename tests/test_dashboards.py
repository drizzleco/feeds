from client import client
from test_register import register


def get_dashboard(client, slug):
    return client.get("/api/dashboards/" + slug)


def get_dashboards(client):
    return client.get("/api/dashboards")


def create_dashboard(client, name=""):
    return client.post(
        "/api/dashboards/new",
        json={"name": name},
    )


def update_dashboard(client, slug, name=""):
    return client.put(
        "/api/dashboards/" + slug,
        json={"name": name},
    )


def delete_dashboard(client, slug):
    return client.delete("/api/dashboards/" + slug)


def test_get_dashboards_returns_empty(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = get_dashboards(client)
    assert not resp.json


def test_get_dashboards_returns_dashboards(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test")
    resp = get_dashboards(client)
    result = {
        "feeds": [],
        "id": 1,
        "name": "test",
        "owner": "username",
        "slug": "test",
    }
    assert any([(k, v) in result.items() for (k, v) in resp.json[0].items()])


def test_get_dash_doesnt_exist_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = get_dashboard(client, "blah")
    assert resp.json.get("error") == "Dashboard doesn't exist!"


def test_create_dash_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_dashboard(client, "test")
    assert resp.json.get("message") == "Dashboard created successfully!"


def test_create_duplicate_dash_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test")
    resp = create_dashboard(client, "test")
    assert resp.json.get("error") == "A dashboard with that name already exists!"


def test_create_dash_no_name_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = create_dashboard(client)
    assert resp.json.get("error") == "Name is required."


def test_update_dash_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test")
    update_dashboard(client, "test", "tester")
    resp = get_dashboard(client, "tester")
    assert resp.json.get("slug") == "tester"


def test_update_nonexistent_dash_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = update_dashboard(client, "blah", "test")
    assert resp.json.get("error") == "Dashboard doesn't exist!"


def test_update_dash_no_name_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test")
    resp = update_dashboard(client, "test")
    assert resp.json.get("error") == "Name is required."


def test_delete_dash_succeeds(client):
    register(client, "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test")
    resp = delete_dashboard(client, "test")
    assert resp.json.get("message") == "Dashboard deleted!"


def test_delete_nonexistent_dash_fails(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = delete_dashboard(client, "blah")
    assert resp.json.get("error") == "Dashboard doesn't exist!"
