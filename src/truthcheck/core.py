from typing import Any


def is_truthy(value: Any) -> bool:
    """Evaluate the truthiness of any Python object."""
    return bool(value)
