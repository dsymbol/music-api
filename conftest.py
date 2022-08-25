import pytest
import requests


@pytest.fixture
def api_client():
    class Client:
        def __init__(self, endpoint):
            self.BASE_URI = f"http://127.0.0.1:5000/{endpoint}"
            self.headers = {"Content-Type": "application/json"}

        def get_all(self, params=None):
            r = requests.get(f"{self.BASE_URI}", headers=self.headers, params=params)
            return r

        def get(self, id):
            r = requests.get(
                f"{self.BASE_URI}/{id}",
                headers=self.headers,
            )
            return r

        def create(self, payload):
            p = requests.post(
                f"{self.BASE_URI}",
                json=payload,
                headers=self.headers,
            )
            return p

        def delete(self, id):
            d = requests.delete(
                f"{self.BASE_URI}/{id}",
                headers=self.headers,
            )
            return d

        def update(self, id, payload):
            p = requests.put(
                f"{self.BASE_URI}/{id}",
                json=payload,
                headers=self.headers,
            )
            return p

        def partially_update(self, id, payload):
            p = requests.patch(
                f"{self.BASE_URI}/{id}",
                json=payload,
                headers=self.headers,
            )
            return p

    return Client


@pytest.fixture
def payload():
    class Payload:
        artist = {
            "name": "Future",
            "first_name": "Nayvadius",
            "last_name": "Wilburn",
            "phone": "412-546-6931",
            "website": "futurefreebandz.com",
            "is_group": False,
        }
        album = {"artist_id": 5, "name": "X&Y"}
        song = {"album_id": 4, "name": "Foreign", "duration": 2.22}

    return Payload
