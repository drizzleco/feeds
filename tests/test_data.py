from client import client
from test_register import register
from test_dashboards import create_dashboard
from test_feeds import create_feed


def create_data(client, feed_slug="", value="", token=""):
    json = {"value": value}
    if token:
        json["token"] = token
    return client.post(f"/api/feeds/{feed_slug}/data", json=json)


def get_data(client, feed_slug="", last=0):
    url = f"/api/feeds/{feed_slug}/data"
    if last:
        url += "?last=" + str(last)
    return client.get(url)


def delete_data(client, feed_slug="", data_id=""):
    return client.delete(f"/api/feeds/{feed_slug}/data/{data_id}")


def test_create_data_text_succeeds(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = create_data(client, "test-feed", "test value")
    assert resp.json.get("message") == "Data posted!"


def test_create_data_number_succeeds(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    resp = create_data(client, "test-feed", "100")
    assert resp.json.get("message") == "Data posted!"


def test_create_data_boolean_succeeds(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "boolean", "test-dash")
    resp = create_data(client, "test-feed", "true")
    assert resp.json.get("message") == "Data posted!"


def test_create_data_image_succeeds(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "image", "test-dash")
    resp = create_data(client, "test-feed", "https://image-url.com/my-image-is-here")
    assert resp.json.get("message") == "Data posted!"


def test_create_data_nonexistent_feed_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    resp = create_data(client, "blah", "test value")
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_create_data_no_value_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "text", "test-dash")
    resp = create_data(client, "test-feed")
    assert resp.json.get("error") == "Value is required."


def test_create_data_not_number_value_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    resp = create_data(client, "test-feed", "100e3")
    assert (
        resp.json.get("error")
        == "Invalid value. Type 'number' was expected but got '100e3'."
    )


def test_create_data_not_boolean_value_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "boolean", "test-dash")
    resp = create_data(client, "test-feed", "truee")
    assert (
        resp.json.get("error")
        == "Invalid value. Type 'boolean' was expected but got 'truee'."
    )


def test_create_data_not_image_value_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "image", "test-dash")
    resp = create_data(client, "test-feed", "httsimage-url.com/.brokemy-image-is-here")
    assert (
        resp.json.get("error")
        == "Invalid value. Type 'image' was expected but got 'httsimage-url.com/.brokemy-image-is-here'."
    )


def test_create_data_on_another_users_feed_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test-dash")
    create_feed(client, "test", "image", "test-dash")
    register(client, "name", "not-test", "nottest@gmail.com", "test", "test")
    resp = create_data(client, "test", "test value")
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_get_data_succeeds(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    create_data(client, "test-feed", "1")
    create_data(client, "test-feed", "2")
    create_data(client, "test-feed", "3")
    resp = get_data(client, "test-feed")
    assert any(
        [
            data["id"] in range(4) and data["value"] in ["1", "2", "3"]
            for data in resp.json.get("data")
        ]
    )


def test_get_data_returns_in_order_of_created_date(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    create_data(client, "test-feed", "1")
    create_data(client, "test-feed", "2")
    create_data(client, "test-feed", "3")
    resp = get_data(client, "test-feed")
    dates = [data["created"] for data in resp.json.get("data")]
    assert dates == sorted(dates, reverse=True)


def test_get_data_nonexistent_feed_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    resp = get_data(client, "blah", "test value")
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_get_data_not_int_for_last_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    create_data(client, "test-feed", "1")
    resp = get_data(client, "test-feed", "asdf")
    assert resp.json.get("error") == "Last must be an integer!"


def test_get_data_on_another_users_feed_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test-dash")
    create_feed(client, "test", "image", "test-dash")
    register(client, "name", "not-test", "nottest@gmail.com", "test", "test")
    resp = get_data(client, "test")
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_delete_data_succeeds(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    create_data(client, "test-feed", "1")
    resp = delete_data(client, "test-feed", 1)
    assert resp.json.get("message") == "Data point deleted!"


def test_delete_data_nonexistent_feed_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    resp = delete_data(client, "blah", 1)
    assert resp.json.get("error") == "Feed doesn't exist!"


def test_delete_data_nonexistent_data_id_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test dash")
    create_feed(client, "test feed", "number", "test-dash")
    resp = delete_data(client, "test-feed", 1)
    assert resp.json.get("error") == "Data point doesn't exist!"


def test_delete_data_on_another_users_feed_fails(client):
    register(client, "name", "test", "test@gmail.com", "test", "test")
    create_dashboard(client, "test-dash")
    create_feed(client, "test", "image", "test-dash")
    create_data(client, "test", "test value")
    register(client, "name", "not-test", "nottest@gmail.com", "test", "test")
    resp = delete_data(client, "test", 1)
    assert resp.json.get("error") == "Feed doesn't exist!"
