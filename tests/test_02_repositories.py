from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

import pytest

from tests.schemas import Book, BookInDB


class BookRepository(ABC):

    @abstractmethod
    def add(self, book: Book) -> BookInDB:
        raise NotImplementedError

    @abstractmethod
    def get(self, book_id: UUID) -> BookInDB:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[BookInDB]:
        raise NotImplementedError


class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.books = dict()

    def add(self, new_book: Book) -> BookInDB:
        if not isinstance(new_book, Book):
            raise ValueError("This repository only accepts Book objects.")
        book = BookInDB(**new_book.dict())
        self.books[book.id] = book
        return book

    def get(self, book_id: UUID) -> Optional[BookInDB]:
        return self.books.get(book_id, None)

    def list(self) -> List[BookInDB]:
        return [book for book_id, book in self.books.items()]


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
