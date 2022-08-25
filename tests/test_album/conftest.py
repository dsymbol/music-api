import pytest


@pytest.fixture
def client(api_client):
    return api_client("api/album")


@pytest.fixture
def payload(payload):
    return payload.album
