from typing import Optional

def strip_whitespace(v: str) -> str:
    """Strips leading and trailing whitespace from a string."""
    if isinstance(v, str):
        return v.strip()
    return v


def strip_whitespace_and_validate(v: Optional[str]) -> Optional[str]:
    """Strips whitespace and ensures the string contains at least 1 non-whitespace character."""
    if isinstance(v, str):
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title must have at least 1 non-whitespace character")
        return stripped
    return v
