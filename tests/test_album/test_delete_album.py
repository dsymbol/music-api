import pytest
import requests

to_delete = [(1, 200), (2, 200), (4, 200)]


@pytest.mark.parametrize("album, status", to_delete)
def test_delete_album(album, status, client):
    response = client.delete(album)
    assert response.status_code == status


def test_delete_invalid_album(client):
    response = client.delete(23)
    assert response.status_code == 404 and response.json()["message"] == "Not Found"


def test_delete_albums_on_artist_delete(client):
    requests.delete("http://127.0.0.1:5000/api/artist/2")
    assert "not found" in client.get(4).text.lower()
