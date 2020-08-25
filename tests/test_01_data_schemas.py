from typing import Optional

import pytest
from pydantic import BaseModel, constr, confloat, ValidationError


class Book(BaseModel):
    title: str
    author: constr(min_length=1, regex="[A-Za-z ,.'-]+$")
    price: confloat(gt=0)
    year: Optional[int]


def test_create_book_with_valid_schema_successfully() -> None:
    book = Book(title="This is a nice book", author="Jane Appleseed", price=18.99, year=1856)
    assert book.title == "This is a nice book"
    assert book.author == "Jane Appleseed"
    assert book.year == 1856
    assert book.price == "Jane Appleseed"


def test_create_book_with_invalid_schema_raises_exception() -> None:
    with pytest.raises(ValidationError):
        Book(author="Lewis Carroll", price=18.99),
