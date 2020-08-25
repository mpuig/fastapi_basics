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
    def add(self, new_book: Book) -> Book:
        pass

    def get(self, book_id: UUID) -> Book:
        pass

    def list(self) -> List[Book]:
        pass


def test_in_memory_repository_created_successfully():
    repo = InMemoryBookRepository()
    assert type(repo) == InMemoryBookRepository
