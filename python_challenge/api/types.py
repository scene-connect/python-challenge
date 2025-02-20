import pydantic

from ..types.home import Home
from ..types.retrofit_planner import RetrofitPlannerResponsePublic


class HomeDetailsResponse(pydantic.BaseModel):
    home: Home


class RetrofitPlannerResponse(pydantic.BaseModel):
    results: RetrofitPlannerResponsePublic

