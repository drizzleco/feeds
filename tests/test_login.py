from client import client
from test_register import register


def login(client, username="", password=""):
    return client.post(
        "/login",
        json={"username": username, "password": password},
        follow_redirects=True,
    )


def test_login_fails_missing_json(client):
    resp = client.post(
        "/login",
        follow_redirects=True,
    )
    assert resp.json.get("error") == "Missing JSON in request"


def test_login_fails_on_no_username(client):
    resp = login(client)
    assert resp.json.get("error") == "Username is required."


def test_login_fails_on_no_password(client):
    resp = login(client, "username")
    assert resp.json.get("error") == "Password is required."


def test_login_fails_user_not_found(client):
    resp = login(client, "username", "password")
    assert resp.json.get("error") == "User not found."


def test_login_fails_invalid_password(client):
    register(client, "name", "username", "username@gmail.com", "password", "password")
    resp = login(client, "username", "notmypassword")
    assert resp.json.get("error") == "Invalid password."


def test_username_login_succeeds(client):
    register(client, "name", "username", "username@gmail.com", "password", "password")
    resp = login(client, "username", "password")
    assert resp.json.get("message") == "Successfully logged in!"


def test_email_login_succeeds(client):
    register(client, "name", "username", "username@gmail.com", "password", "password")
    resp = login(client, "username@gmail.com", "password")
    assert resp.json.get("message") == "Successfully logged in!"
