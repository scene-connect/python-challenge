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
from .types import HomeDetailsResponse, EnergyProfileCompareResponse

UPRN_NOT_FOUND = """The UPRN can not be found in the OS Open UPRN database.
This may mean the UPRN is incorrect, or that the building was
constructed recently and the UPRN has not been published yet."""

UUID_NOT_FOUND = """The UUID not found"""


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
            home = get_home(uprn=uprn)
        except FileNotFoundError:
            raise NotFound(detail=UPRN_NOT_FOUND)
        except pydantic.ValidationError as error:
            raise ValidationError(detail=str(error))

        response = HomeDetailsResponse(
            home=home,
        )
        return Response(data=response.model_dump(mode="json"))

class ChartReports(APIView):
    UUID = "uuid"
    http_method_names = ["get"]
    description = markdown(
        """
    Get the comparison report for annual C02 usage before and after improvements.
    """
    )

    @extend_schema(
        responses={
            "200": OpenApiResponse(
                response=EnergyProfileCompareResponse,
            ),
            "400": OpenApiResponse(
                description="Validation error (e.g. non-numeric UUID)",
            ),
            "404": OpenApiResponse(description=UUID_NOT_FOUND),
        },
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        uuid = self.kwargs[UUID]
        reponse = self.retrieveChartReports("uuid")
        return Response(data=response.model_dump(mode="json"))

    def retrieveChartReports(self, uuid):
        try:
            retroFitPlannerModel = get_results(uuid)
        except FileNotFoundError:
            raise NotFound(detail=UUID_NOT_FOUND)
        except pydantic.ValidationError as error:
            raise ValidationError(detail=str(error))

        monthlyEnergyDict = retroFitPlannerModel.baseline_energy_profile.monthly_energy_total
        improvedMonthlyEnergyDict = retroFitPlannerModel.improvement_plan[0].energy_profile.monthly_energy_total

        originalC02ReductionList = monthlyEnergyDict.values()
        improvedC02ReductionList = improvedMonthlyEnergyDict.values()
        keyMonths = monthlyEnergyDict.keys()
        return EnergyProfileCompareResponse(
            months = keyMonths,
            originalC02Reduction = originalC02ReductionList,
            improvedC02Reduction = improvedC02ReductionList
        )