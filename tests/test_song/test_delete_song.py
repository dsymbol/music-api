import pytest
import requests

to_delete = [(1, 200), (2, 200), (5, 200)]


@pytest.mark.parametrize("song, status", to_delete)
def test_delete_song(song, status, client):
    response = client.delete(song)
    assert response.status_code == status


def test_delete_invalid_song(client):
    response = client.delete(23)
    assert response.status_code == 404 and response.json()["message"] == "Not Found"


def test_delete_songs_on_artist_delete(client):
    requests.delete("http://127.0.0.1:5000/api/artist/2")
    assert "not found" in client.get(3).text.lower()
