from contextlib import closing
from typing import List
from uuid import UUID, uuid4

import pytest
from sqlalchemy import Column, String
from sqlalchemy.engine import Connection, create_engine
from sqlalchemy.ext.declarative import declarative_base
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


Base = declarative_base()


class BookModel(Base):
    __tablename__ = 'books'

    # It is not recommended to store uuid as str, but for these tests is ok
    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    title = Column(String)
    author = Column(String)


@pytest.fixture(scope="session")
def db_connection() -> Connection:
    db_url = "sqlite:///:memory:?check_same_thread=False"
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as connection:
        Base.metadata.create_all(bind=connection)
        yield connection
        Base.metadata.drop_all(bind=connection)


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
