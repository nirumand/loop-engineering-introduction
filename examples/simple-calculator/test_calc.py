import pytest

from calc import add, divide, mul


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_mul():
    assert mul(2, 3) == 6


def test_divide():
    assert divide(6, 2) == 3
    assert divide(10, 5) == 2


def test_divide_truncates():
    assert divide(7, 2) == 3
    assert divide(9, 4) == 2


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)
