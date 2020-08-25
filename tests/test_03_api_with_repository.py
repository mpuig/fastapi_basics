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

    @app.post("/", name="books:create-book", status_code=201)
    def create_new_book(
        book: Book,
        books_repo: InMemoryBookRepository = Depends(InMemoryBookRepository)
    ) -> Book:
        book_db = books_repo.add(book)
        return book_db

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_get_all_books_successfully(app, client) -> None:
    url_get_books = app.url_path_for("books:get-all-books")
    response_get_books = client.get(url_get_books)
    assert response_get_books.status_code == 200


def test_create_valid_book_successfully(app, client, a_book) -> None:
    url_create_book = app.url_path_for("books:create-book")
    response_new_book = client.post(url_create_book, json={'book': a_book.dict()})
    assert response_new_book.status_code == 201

    new_book_json = response_new_book.json()
    assert isinstance(new_book_json, dict)

    assert 'id' in new_book_json
    assert len(new_book_json['id']) == 36

    assert a_book == Book(**new_book_json)


def test_invalid_create_book_raises_error(app, client) -> None:
    url_create_book = app.url_path_for("books:create-book")
    empty_payload = {}
    response_new_book = client.post(url_create_book, json=empty_payload)
    assert response_new_book.status_code == 422
