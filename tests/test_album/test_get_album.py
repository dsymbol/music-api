import pytest

albums = [(6, 200), (7, 200), (64, 404)]


@pytest.mark.parametrize("album_id, status", albums)
def test_get_album_by_id(album_id, status, client):
    response = client.get(album_id)
    assert response.status_code == status


def test_get_albums(client):
    data = ["Take Care", "Off the Wall", "Help!"]
    response = client.get_all()
    assert all(i in response.text for i in data)


def test_get_album_songs(client):
    response = client.get("6/songs")
    assert "Rock With You" in response.text and response.status_code == 200


def test_get_albums_using_params(client):
    response = client.get_all(params={"id": 2})
    assert response.json()[0]["artist_id"] == 1 and response.status_code == 200
    response = client.get_all(params={"artist_id": "7"})
    assert "Dying to Live" in response.text and response.status_code == 200
    response = client.get_all(params={"name": "Help!"})
    assert response.json()[0]["album_id"] == 11 and response.status_code == 200
