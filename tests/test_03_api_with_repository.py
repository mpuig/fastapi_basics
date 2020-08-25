import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app():
    app = FastAPI()

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_get_all_books_successfully(app, client) -> None:
    url_get_books = app.url_path_for("books:get-all-books")
    response_get_books = client.get(url_get_books)
    assert response_get_books.status_code == 200
