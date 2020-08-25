from fastapi import Depends

from tests.repositories import InMemoryBookRepository


class BookPaginationService:
    page_size = 10

    def __init__(self, repository: InMemoryBookRepository = Depends(InMemoryBookRepository)):
        self.repository = repository

    def get_page(self, num=1) -> dict:
        content = self.repository.list(skip=num - 1, offset=self.page_size)
        return dict(page=num, page_size=self.page_size, content=content)
