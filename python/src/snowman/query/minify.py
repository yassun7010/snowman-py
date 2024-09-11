import re

SPACE_PATTERN = re.compile(r"\s+")


def minify(query: str) -> str:
    """
    Minify the given query.

    #### Usage:
        ```python
        minify("SELECT * FROM database.schema.users")
        ```
    """
    return re.sub(SPACE_PATTERN, " ", query.replace("\n", "")).strip()
