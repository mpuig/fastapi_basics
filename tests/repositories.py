from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

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
