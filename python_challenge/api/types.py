import pydantic

from ..types.home import Home


class HomeDetailsResponse(pydantic.BaseModel):
    home: Home


class EnergyProfileCompareResponse(pydantic.BaseModel):
    months: list[int]
    originalC02Reduction: list[float]
    improvedC02Reduction: list[float]