def test_create_song(client, payload):
    response = client.create(payload)
    assert (
            response.status_code == 201 and response.json()[0]["name"].lower() == "foreign"
    )


def test_create_existing_song(client, payload):
    payload["song_id"] = 1
    response = client.create(payload)
    assert response.status_code == 409 and "conflict" in response.text


def test_create_song_invalid_payload(client):
    payload = {"Hello": "World"}
    response = client.create(payload)
    assert response.status_code == 422
