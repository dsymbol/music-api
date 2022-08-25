def test_create_artist(client, payload):
    response = client.create(payload)
    assert (
            response.status_code == 201
            and response.json()[0]["name"].lower() == "future"
    )


def test_create_existing_artist(client, payload):
    payload["artist_id"] = 1
    response = client.create(payload)
    assert response.status_code == 409 and "conflict" in response.text


def test_create_artist_invalid_payload(client):
    payload = {"Hello": "World"}
    response = client.create(payload)
    assert response.status_code == 422
