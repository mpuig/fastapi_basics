from uuid import UUID

import pytest

from tests.repositories import InMemoryBookRepository
from tests.schemas import Book


def test_in_memory_repository_created_successfully():
    repo = InMemoryBookRepository()
    assert type(repo) == InMemoryBookRepository


def test_in_memory_repository_initially_empty_successfully():
    repo = InMemoryBookRepository()
    items = repo.list()
    assert len(items) == 0


def test_add_valid_data_to_in_memory_repository_successfully(a_book):
    repo = InMemoryBookRepository()
    repo.add(a_book)
    items = repo.list()
    assert len(items) == 1
    assert isinstance(items[0], Book)
    assert items[0].title == a_book.title
    assert items[0].author == a_book.author


def test_add_invalid_data_to_n_memory_repository_raises_exception():
    repo = InMemoryBookRepository()
    a_dictionary = dict(title="Foo", author="Boo")
    with pytest.raises(ValueError):
        repo.add(a_dictionary)

    items = repo.list()
    assert len(items) == 0


def test_get_book_by_id_from_in_memory_repository_successfully(a_book, another_book):
    repo = InMemoryBookRepository()
    book1 = repo.add(a_book)
    book2 = repo.add(another_book)

    response1 = repo.get(book_id=book1.id)
    assert response1 == book1
    assert response1.title == a_book.title

    response2 = repo.get(book_id=book2.id)
    assert response2 == book2
    assert response2.title == another_book.title


def test_get_book_by_id_from_in_memo_repository_with_invalid_id_returns_none(a_book):
    repo = InMemoryBookRepository()
    repo.add(a_book)

    invalid_id = UUID('00000000-0000-0000-0000-000000000000')
    response1 = repo.get(book_id=invalid_id)
    assert response1 is None
