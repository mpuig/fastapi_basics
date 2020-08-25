from contextlib import closing
from typing import List
from uuid import UUID

import pytest
from sqlalchemy.engine import Connection, create_engine
from sqlalchemy.orm import Session, sessionmaker

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


@pytest.fixture(scope="session")
def db_connection() -> Connection:
    db_url = "sqlite:///:memory:?check_same_thread=False"
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as connection:
        yield connection


@pytest.fixture(scope="function")
def db_session(db_connection: Connection) -> Session:
    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)
    with closing(session_maker()) as session:
        yield session


def test_create_new_book_in_sql_repository_successfully(db_session: Session, a_book) -> None:
    repo = SQLBookRepository(db_session)
    created_book = repo.add(book=a_book)
    assert created_book
    assert isinstance(created_book, BookInDB)
    assert created_book.title == a_book.title
    assert created_book.author == a_book.author
