import pytest

from tests.repositories import InMemoryBookRepository
from tests.schemas import Book


def get_repo_test() -> InMemoryBookRepository:
    repo_test = InMemoryBookRepository(initial_books=dict())
    for book_id in range(0, 25):
        repo_test.add(Book(title=f"title {book_id}", author=f"author {book_id}"))
    return repo_test


@pytest.mark.parametrize(
    "page_num, results_count, expected_status", (
        (1, 10, 200),
        (3, 5, 200),
        (5, 0, 200),
        (1000, 0, 200),
    ),
)
def test_pagination_service_successfully(app, client, page_num, results_count, expected_status) -> None:
    app.dependency_overrides[InMemoryBookRepository] = get_repo_test

    response = client.get(f"/books?page_num={page_num}")
    assert response.status_code == expected_status

    content = response.json()
    assert "page" in content
    assert content["page"] == page_num
    assert "content" in content
    assert len(content["content"]) == results_count


@pytest.mark.parametrize(
    "page_num, expected_status", (
        (-1, 422),
        (0, 422),
        ('0', 422),
        ('a', 422),
    ),
)
def test_pagination_service_fails(app, client, page_num, expected_status) -> None:
    app.dependency_overrides[InMemoryBookRepository] = get_repo_test

    response = client.get(f"/books?page_num={page_num}")
    assert response.status_code == expected_status
