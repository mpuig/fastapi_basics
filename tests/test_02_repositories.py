from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str
    author: str


class BookInDB(Book):
    id: UUID = Field(default_factory=uuid4)


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
    books = dict()  # this sets a class-level attribute, common to all instances of `InMemoryBooksRepository`

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


@pytest.fixture()
def a_book() -> Book:
    return Book(title="A nice title", author="John Smith")


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
