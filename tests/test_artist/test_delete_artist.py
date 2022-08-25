import pytest

to_delete = [(1, 200), (2, 200), (4, 200)]


@pytest.mark.parametrize("artist, status", to_delete)
def test_delete_artist(artist, status, client):
    response = client.delete(artist)
    assert response.status_code == status


def test_delete_invalid_artist(client):
    response = client.delete(23)
    assert response.status_code == 404 and response.json()["message"] == "Not Found"
