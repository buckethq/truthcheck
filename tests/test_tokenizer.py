import pytest

from truthcheck.tokenizer import count_tokens, print_token_count


def test_count_tokens_basic() -> None:
    assert count_tokens("hello world") > 0
    assert count_tokens("") == 0


def test_count_tokens_non_string() -> None:
    assert count_tokens(42) >= 1
    assert count_tokens([1, 2, 3]) >= 1


def test_print_token_count(capsys: pytest.CaptureFixture) -> None:
    count = print_token_count("test")
    captured = capsys.readouterr()
    assert "🔢 Token count (cl100k_base):" in captured.out
    assert isinstance(count, int)
