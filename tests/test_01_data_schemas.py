import pytest
from pydantic import ValidationError


def test_create_book_with_valid_schema_successfully() -> None:
    book = Book(title="This is a nice book", author="Jane Appleseed", price=18.99, year=1856)
    assert book.title == "This is a nice book"
    assert book.author == "Jane Appleseed"
    assert book.year == 1856
    assert book.price == "Jane Appleseed"


def test_create_book_with_invalid_schema_raises_exception() -> None:
    with pytest.raises(ValidationError):
        Book(author="Lewis Carroll", price=18.99),
