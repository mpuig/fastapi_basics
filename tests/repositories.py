from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from tests.models import BookModel
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
    books = dict()

    def __init__(self, initial_books: dict = None):
        if initial_books is not None:
            self.books = initial_books

    def add(self, new_book: Book) -> BookInDB:
        if not isinstance(new_book, Book):
            raise ValueError("This repository only accepts Book objects.")
        book = BookInDB(**new_book.dict())
        self.books[book.id] = book
        return book

    def get(self, book_id: UUID) -> Optional[BookInDB]:
        return self.books.get(book_id, None)

    def list(self, skip=0, offset=5) -> List[BookInDB]:
        return list(self.books.values())[skip * offset:(skip + 1) * offset]


class SQLBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, book: Book) -> BookInDB:
        book_data = jsonable_encoder(book)
        book = BookModel(**book_data)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return BookInDB(**book.__dict__)

    def get(self, book_id: UUID) -> BookInDB:
        book = self.db.query(BookModel).filter(BookModel.id == str(book_id)).first()
        return BookInDB(**book.__dict__)

    def list(self, skip=0, offset=5) -> List[BookInDB]:
        books = self.db.query(BookModel).offset(skip).limit(offset).all()
        return [BookInDB(**book.__dict__) for book in books]
