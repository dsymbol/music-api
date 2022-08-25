import pytest


@pytest.fixture
def client(api_client):
    return api_client("api/artist")


@pytest.fixture
def payload(payload):
    return payload.artist
