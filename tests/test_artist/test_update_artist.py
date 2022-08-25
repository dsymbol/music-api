def test_update_artist(client, payload):
    response = client.update(6, payload)
    assert response.status_code == 200 and response.json()[0]["name"] == "Future"


def test_partially_update_artist(client, payload):
    key, value = "artist_id", 10
    response = client.partially_update(1, {key: value})
    assert response.status_code == 200 and response.json()[0][key] == value


def test_update_artist_no_payload(client):
    response = client.update(1, {})
    assert response.status_code == 422
