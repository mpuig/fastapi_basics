from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BookModel(Base):
    __tablename__ = 'books'

    # It is not recommended to store uuid as str, but for these tests is ok
    id = Column(String, primary_key=True, index=True, default=lambda x: str(uuid4()))
    title = Column(String)
    author = Column(String)
