from decimal import Decimal
from enum import Enum
from typing import Annotated
from typing import Final
from typing import Literal
from typing import NamedTuple

import pydantic

MonthNumber = Annotated[int, pydantic.Field(ge=1, le=12)]


class EmptyRange(NamedTuple):
    # drf_extra_fields represents empty ranges as {"empty": true} instead of JSON null.
    empty: bool = True


class RangeIntDetailed(NamedTuple):
    """
    Detailed integer range type, matching how Django exports a RangeField[int].
    Compatible with a tuple[int, int, str] for getting the range boundaries by index
    like the simpler RangeInt.
    """

    lower: int | None
    upper: int | None
    bounds: str


RangeInt = tuple[int | None, int | None] | RangeIntDetailed | EmptyRange

DecimalFraction = Annotated[Decimal, pydantic.Field(ge=0, le=1)]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


T_ParkHome = Literal["park home"]

PARK_HOME: Final[T_ParkHome] = "park home"
"""
Park homes have their own building standards, separate from their EPC country.
"""

EfficiencyRatingBand = Literal["A", "B", "C", "D", "E", "F", "G"]


YearRange = RangeInt
"""
Building age bands by year of construction, from-to, inclusive.

If either value is None then it will be treated as infinite time in that direction,
e.g. (None, 2002) represents all years prior to and including 2002.
"""
