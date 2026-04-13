import pytest

from truthcheck2.core import is_truthy


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, False),
        (1, True),
        ("", False),
        ("hello", True),
        ([], False),
        ([1], True),
        ({}, False),
        ({"a": 1}, True),
        (None, False),
        (False, False),
        (True, True),
        (0.0, False),
        (0.1, True),
    ],
)
def test_is_truthy(value: object, expected: bool) -> None:
    assert is_truthy(value) is expected
