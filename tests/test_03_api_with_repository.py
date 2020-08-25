from typing import List

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from tests.repositories import InMemoryBookRepository
from tests.schemas import Book


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/", name="books:get-all-books")
    def get_all_books(
        books_repo: InMemoryBookRepository = Depends(InMemoryBookRepository)
    ) -> List[Book]:
        books = books_repo.list()
        return books

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_get_all_books_successfully(app, client) -> None:
    url_get_books = app.url_path_for("books:get-all-books")
    response_get_books = client.get(url_get_books)
    assert response_get_books.status_code == 200
