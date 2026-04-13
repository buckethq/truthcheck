from typing import Any

import tiktoken


def count_tokens(value: Any, model: str = "cl100k_base") -> int:
    """Count tokens in the string representation of any object."""
    try:
        encoding = tiktoken.get_encoding(model)
    except Exception as e:
        raise ValueError(f"Failed to load tiktoken model '{model}': {e}") from e

    try:
        text = str(value)
    except Exception as e:
        raise TypeError(f"Cannot convert {type(value).__name__} to string: {e}") from e

    return len(encoding.encode(text))


def print_token_count(value: Any, model: str = "cl100k_base") -> int:
    """Print and return the token count for any object."""
    count = count_tokens(value, model)
    print(f"🔢 Token count ({model}): {count}")
    return count
