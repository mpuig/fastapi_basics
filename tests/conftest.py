import pytest

from tests.schemas import Book


@pytest.fixture()
def a_book() -> Book:
    return Book(title="A nice title", author="John Smith")


@pytest.fixture()
def another_book() -> Book:
    return Book(title="Another nice title", author="Jane Boo")
