from typing import Any

def is_truthy(value: Any) -> bool:
    """Evaluate the truthiness of any Python object.
    
    Uses Python's standard boolean coercion but is explicitly typed
    and documented for package consumers.
    
    Args:
        value: Any Python object.
        
    Returns:
        True if the value is truthy, False otherwise.
    """
    return bool(value)