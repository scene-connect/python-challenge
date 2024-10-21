import pydantic

from ..types.home import Home


class HomeDetailsResponse(pydantic.BaseModel):
    home: Home
