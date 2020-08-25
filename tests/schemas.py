from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str
    author: str


class BookInDB(Book):
    id: UUID = Field(default_factory=uuid4)
