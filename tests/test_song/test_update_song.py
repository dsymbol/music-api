def test_update_song(client, payload):
    response = client.update(5, payload)
    assert response.status_code == 200 and response.json()[0]["name"] == "Foreign"


def test_partially_update_song(client, payload):
    key, value = "album_id", 3
    response = client.partially_update(9, {key: value})
    assert response.status_code == 200 and response.json()[0][key] == value


def test_update_song_no_payload(client):
    response = client.update(1, {})
    assert response.status_code == 422
