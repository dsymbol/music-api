import pytest
from cerberus import Validator


@pytest.fixture
def v():
    schema = {
        "artist_id": {"type": "integer", "required": True},
        "name": {"type": "string", "required": True},
        "first_name": {"nullable": True, "type": "string", "required": False},
        "last_name": {"nullable": True, "type": "string", "required": False},
        "phone": {"nullable": True, "type": "string", "required": False},
        "website": {"nullable": True, "type": "string", "required": False},
        "is_group": {"nullable": True, "type": "boolean", "required": False},
    }
    return Validator(schema)


def test_one_artist_schema(client, v):
    response = client.get(1).json()
    assert v.validate(response[0])


def test_all_artist_schema(client, v):
    artists = client.get_all().json()
    for artist in artists:
        assert v.validate(artist)
