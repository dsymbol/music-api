import pytest

artists = [(6, 200), (8, 200), (10, 404)]


@pytest.mark.parametrize("artist_id, status", artists)
def test_get_artist_by_id(artist_id, status, client):
    response = client.get(artist_id)
    assert response.status_code == status


def test_get_artists(client):
    data = ["Lil Uzi Vert", "Yeat", "coldplay.com", "thebeatles.com"]
    response = client.get_all()
    assert all(i in response.text for i in data)


def test_get_artist_albums(client):
    response = client.get("2/albums")
    assert "die lit" in response.text.lower() and response.status_code == 200


def test_get_artist_songs(client):
    response = client.get("6/songs")
    assert (
            all(i in response.text.lower() for i in ["poppin", "cmon"])
            and response.status_code == 200
    )


def test_get_artists_using_params(client):
    response = client.get_all(params={"id": 2})
    assert (
            response.json()[0]["first_name"].lower() == "jordan"
            and response.status_code == 200
    )
    response = client.get_all(params={"name": "coldplay"})
    assert "coldplay.com" in response.text.lower() and response.status_code == 200
    response = client.get_all(params={"first_name": "Noah"})
    assert "yeat" in response.text.lower() and response.status_code == 200
    response = client.get_all(params={"last_name": "Jackson"})
    assert (
            response.json()[0]["first_name"].lower() == "michael"
            and response.status_code == 200
    )
    response = client.get_all(params={"group": True})
    assert len(response.json()) == 2 and response.status_code == 200
