import pytest
from cerberus import Validator


@pytest.fixture
def v():
    schema = {
        "song_id": {"type": "integer", "required": True},
        "album_id": {"type": "integer", "required": True},
        "name": {"type": "string", "required": True},
        "duration": {"nullable": True, "type": "float", "required": False},
    }
    return Validator(schema)


def test_one_song_schema(client, v):
    response = client.get(3).json()
    assert v.validate(response[0])


def test_all_song_schema(client, v):
    songs = client.get_all().json()
    for song in songs:
        assert v.validate(song)
