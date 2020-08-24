import pytest


def sum_integers(x: int, y: int) -> int:
    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Parameters 'x' and 'y' must be integers.")
    return x + y


def test_sum_integers_with_correct_values_successfully():
    result = sum_integers(1, 3)
    assert result == 4


def test_sum_integers_with_strings_fails():
    with pytest.raises(ValueError):
        sum_integers('1', '3')


def test_sum_integers_with_floats_fails():
    with pytest.raises(ValueError):
        sum_integers(1.0, 3.0)
