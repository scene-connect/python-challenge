import pydantic
from .home import HomePartial


class HomeDetailsResponse(pydantic.BaseModel):
    home: HomePartial
