"""truthcheck: Evaluate truthiness and count tokens for any Python object."""

__version__ = "0.1.0"

from .core import is_truthy
from .tokenizer import count_tokens, print_token_count

__all__ = ["is_truthy", "count_tokens", "print_token_count"]
