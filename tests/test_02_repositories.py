from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


class Book(object):
    pass


class BookRepository(ABC):

    @abstractmethod
    def add(self, book: Book) -> Book:
        raise NotImplementedError

    @abstractmethod
    def get(self, book_id: UUID) -> Book:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Book]:
        raise NotImplementedError


class InMemoryBookRepository(BookRepository):
    books = dict()  # this sets a class-level attribute, common to all instances of `InMemoryBooksRepository`

    def add(self, new_book: Book) -> Book:
        pass

    def get(self, book_id: UUID) -> Book:
        pass

    def list(self) -> List[Book]:
        return [book for book_id, book in self.books.items()]


def test_in_memory_repository_created_successfully():
    repo = InMemoryBookRepository()
    assert type(repo) == InMemoryBookRepository


def test_in_memory_repository_initially_empty_successfully():
    repo = InMemoryBookRepository()
    items = repo.list()
    assert len(items) == 0
