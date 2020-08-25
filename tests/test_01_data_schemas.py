from typing import Optional

import pytest
from pydantic import BaseModel, constr, confloat, ValidationError


class Book(BaseModel):
    title: str
    author: constr(min_length=1, regex="[A-Za-z ,.'-]+$")
    price: confloat(gt=0)
    year: Optional[int]


@pytest.mark.parametrize(
    "valid_schema", (
        dict(title="This is a nice book", author="Jane Appleseed", price=18.99, year=1856),
        dict(title="This is another nice book", author="John Smith", price=18.99)
    ),
)
def test_create_book_with_valid_schema_successfully(valid_schema: dict) -> None:
    book = Book(
        title=valid_schema.get("title"),
        author=valid_schema.get("author"),
        year=valid_schema.get("year"),
        price=valid_schema.get("price"),
    )
    assert book.title == valid_schema.get("title")
    assert book.author == valid_schema.get("author")
    assert book.year == valid_schema.get("year")
    assert book.price == valid_schema.get("price")


@pytest.mark.parametrize(
    "invalid_schema", (
        dict(author="Lewis Carroll", price=18.99),
        dict(title="Another nice book", author="Lewis Carroll"),
        dict(title="Lorem ipsum", author="Lewis Carroll", price=-10.0)
    ),
)
def test_create_book_with_invalid_schema_raises_exception(invalid_schema: dict) -> None:
    with pytest.raises(ValidationError):
        Book(
            title=invalid_schema.get("title"),
            author=invalid_schema.get("author"),
            year=invalid_schema.get("year"),
            price=invalid_schema.get("price"),
        )
