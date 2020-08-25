from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from tests.repositories import BookRepository
from tests.schemas import BookInDB, Book


class SQLBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, book: Book) -> BookInDB:
        pass

    def get(self, book_id: UUID) -> BookInDB:
        pass

    def list(self) -> List[BookInDB]:
        pass


def test_create_new_book_in_sql_repository_successfully(db_session: Session, a_book) -> None:
    repo = SQLBookRepository(db_session)
    created_book = repo.add(book=a_book)
    assert created_book
    assert isinstance(created_book, BookInDB)
    assert created_book.title == a_book.title
    assert created_book.author == a_book.author


