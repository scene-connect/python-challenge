from typing import Any

import pydantic
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from markdown import markdown
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import get_home, get_results
from .types import HomeDetailsResponse, EnergyRunResultsResponse

UPRN_NOT_FOUND = """The UPRN can not be found in the OS Open UPRN database.
This may mean the UPRN is incorrect, or that the building was
constructed recently and the UPRN has not been published yet."""


class HomeDetailsByUPRN(APIView):
    http_method_names = ["get"]
    description = markdown(
        """
Get all the details ZUoS has about a Home, by it's UPRN.
"""
    )

    @extend_schema(
        responses={
            "200": OpenApiResponse(
                response=HomeDetailsResponse,
            ),
            "400": OpenApiResponse(
                description="Validation error (e.g. non-numeric UPRN)",
            ),
            "404": OpenApiResponse(description=UPRN_NOT_FOUND),
        },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        uprn = self.kwargs["uprn"]
        try:
            home = get_home(uprn)
        except FileNotFoundError:
            raise NotFound(detail=UPRN_NOT_FOUND)
        except pydantic.ValidationError as error:
            raise ValidationError(detail=str(error))

        response = HomeDetailsResponse(
            home=home,
        )
        return Response(data=response.model_dump(mode="json"))


UUID_NOT_FOUND = """The UUID can not be found in the ZUoS Retrofit Planner."""

class EnergyByUUID(APIView):
    http_method_names = ["get"]
    description = markdown(
        """
Output from a simulation run by it's UUID.
"""
    )

    @extend_schema(
        responses={
            "200": OpenApiResponse(
                response=HomeDetailsResponse,
            ),
            "400": OpenApiResponse(
                description="Validation error",
            ),
            "404": OpenApiResponse(description=UUID_NOT_FOUND),
        },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        uuid = self.kwargs["uuid"]
        try:
            # home = get_home(uprn)
            energy_run_results = get_results(uuid)
        except FileNotFoundError:
            raise NotFound(detail=UUID_NOT_FOUND)
        except pydantic.ValidationError as error:
            raise ValidationError(detail=str(error))

        response = EnergyRunResultsResponse(
            energy_run_results=energy_run_results,
        )
        return Response(data=response.model_dump(mode="json"))
