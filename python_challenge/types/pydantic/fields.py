from typing import Annotated
from typing import Any

import pydantic


def _uprn_is_numeric(value: Any) -> Any:
    """
    Simple validator for UPRN type.
    Does not need to allow "" or None, this validator only runs if given a value which
    should actually be an UPRN.
    """
    if isinstance(value, str):
        if value.isnumeric():
            return value
    raise ValueError("UPRN must be numeric")


UPRN = Annotated[
    str,
    pydantic.Field(max_length=12, min_length=1),
    pydantic.AfterValidator(_uprn_is_numeric),
]


FloatJSONRound = Annotated[
    float,
    pydantic.PlainSerializer(
        lambda x: round(x, 1), return_type=float, when_used="json"
    ),
]
"""
Float which pydantic will round when serializing to JSON.
"""
