import pytest
from cerberus import Validator


@pytest.fixture
def v():
    schema = {
        "album_id": {"type": "integer"},
        "artist_id": {"type": "integer"},
        "name": {"type": "string"},
    }
    return Validator(schema, require_all=True)


def test_one_album_schema(client, v):
    response = client.get(1).json()
    assert v.validate(response[0])


def test_all_album_schema(client, v):
    albums = client.get_all().json()
    for album in albums:
        assert v.validate(album)
