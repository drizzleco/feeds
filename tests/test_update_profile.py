from client import client
from test_register import register


def update_profile(client, **kwargs):
    return client.put(
        "/me",
        json=kwargs,
    )


def test_update_fails_on_no_json(client):
    resp = client.put("me")
    assert resp.json.get("error") == "Missing JSON in request"


def test_update_fails_on_invalid_email(client):
    register(client, "name", "username", "email", "password", "password")
    resp = update_profile(client, email="email")
    assert resp.json.get("error") == "Invalid email"


def test_update_nonmatching_passwords_fails(client):
    register(client, "name", "username", "email", "password", "password")
    resp = update_profile(client, password="password", confirm="nomatch")
    assert resp.json.get("error") == "Passwords do not match"


def test_update_succeeds(client):
    register(client, "name", "username", "my@email.com", "password", "password")
    resp = update_profile(client, name="tester", username="bob", email="email@google.com")
    assert resp.json.get("message") == "Successfully updated!"
