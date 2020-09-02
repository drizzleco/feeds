from client import client


def register(client, username="", email="", password="", confirm=""):
    return client.post(
        "register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "confirm": confirm,
        },
        follow_redirects=True,
    )


def test_register_fails_on_no_json(client):
    resp = client.post("register")
    assert resp.json.get("error") == "Missing JSON in request"


def test_register_fails_on_no_username(client):
    resp = register(client)
    assert resp.json.get("error") == "Username is required."


def test_register_fails_on_no_email(client):
    resp = register(client, "username", "")
    assert resp.json.get("error") == "Email is required."


def test_register_fails_on_no_password(client):
    resp = register(client, "username", "email")
    assert resp.json.get("error") == "Password is required."


def test_register_fails_on_no_confirm(client):
    resp = register(client, "username", "email", "password")
    assert resp.json.get("error") == "Password confirmation is required."


def test_register_fails_passwords_dont_match(client):
    resp = register(client, "username", "email", "password", "doesntmatch")
    assert resp.json.get("error") == "Passwords do not match"


def test_register_fails_user_exists(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = register(client, "test", "email", "password", "password")
    assert resp.json.get("error") == "User already exists."


def test_register_fails_email_exists(client):
    register(client, "test", "test@gmail.com", "test", "test")
    resp = register(client, "another test", "test@gmail.com", "password", "password")
    assert resp.json.get("error") == "Email already exists."


def test_register_succeeds(client):
    resp = register(client, "test", "test@gmail.com", "test", "test")
    assert resp.json.get("message") == "Successfully registered!"
