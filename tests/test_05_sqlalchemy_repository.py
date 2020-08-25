from contextlib import closing

import pytest
from sqlalchemy.engine import Connection, create_engine
from sqlalchemy.orm import Session, sessionmaker

from tests.models import Base
from tests.repositories import SQLBookRepository
from tests.schemas import BookInDB, Book


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


def test_get_book_from_sql_repository_successfully(db_session: Session, a_book) -> None:
    repo = SQLBookRepository(db_session)
    created_book = repo.add(book=a_book)
    book_from_db = repo.get(book_id=created_book.id)
    assert book_from_db
    assert isinstance(book_from_db, BookInDB)
    assert created_book.id == book_from_db.id
    assert a_book.title == book_from_db.title
    assert a_book.author == book_from_db.author


def test_get_list_of_books_successfully(db_session: Session) -> None:
    repo = SQLBookRepository(db_session)
    for book_id in range(0, 25):
        book = Book(title=f"title {book_id}", author=f"author {book_id}")
        repo.add(book=book)

    books_from_db = repo.list()
    assert books_from_db
    assert len(books_from_db) == 5
