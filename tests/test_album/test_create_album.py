def test_create_album(client, payload):
    response = client.create(payload)
    assert response.status_code == 201 and response.json()[0]["artist_id"] == 5


def test_create_existing_album(client, payload):
    payload["album_id"] = 1
    response = client.create(payload)
    assert response.status_code == 409 and "conflict" in response.text


def test_create_album_invalid_payload(client):
    payload = {"Hello": "World"}
    response = client.create(payload)
    assert response.status_code == 422
