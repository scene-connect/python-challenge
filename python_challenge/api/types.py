import pydantic

from python_challenge.types.retrofit_planner import RetrofitPlannerResponsePublic

from ..types.home import Home


class HomeDetailsResponse(pydantic.BaseModel):
    home: Home

class EnergyRunResultsResponse(pydantic.BaseModel):
    energy_run_results: RetrofitPlannerResponsePublic
