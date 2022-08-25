import pytest

songs = [(6, 200), (8, 200), (45, 404)]


@pytest.mark.parametrize("song_id, status", songs)
def test_get_song_by_id(song_id, status, client):
    response = client.get(song_id)
    assert response.status_code == status


def test_get_songs(client):
    data = ["From the Cradle", "Viva La Vida", "Marvins Room", "Rock With You"]
    response = client.get_all()
    assert all(i in response.text for i in data)


def test_get_songs_using_params(client):
    response = client.get_all(params={"id": 8})
    assert response.json()[0]["song_id"] == 8 and response.status_code == 200
    response = client.get_all(params={"album_id": 11})
    assert response.json()[0]["album_id"] == 11 and response.status_code == 200
    response = client.get_all(params={"name": "long time"})
    assert response.json()[0]["song_id"] == 3 and response.status_code == 200
