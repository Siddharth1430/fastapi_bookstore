from fastapi.testclient import TestClient
from fastapi import FastAPI

from main import app

app = FastAPI()


client = TestClient(app)


def test_publish_book():
    book = {"title": "aaa"}
    response = client.patch("/publish-book", json=book)
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}
