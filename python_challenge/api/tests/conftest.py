from pathlib import Path

import pytest
from rest_framework.test import APIClient

from python_challenge.types.home import Home
from python_challenge.types.retrofit_planner import RetrofitPlannerResponsePublic

PATH_DATA = Path(__file__).parent.parent.parent.parent / "data"


@pytest.fixture
def uprn() -> str:
    return "906205784"


@pytest.fixture
def home() -> Home:
    with open(PATH_DATA / "906205784.json") as file:
        return Home.model_validate_json(file.read())


@pytest.fixture
def run_id() -> str:
    return "a0ce4c08-6ca3-46f9-8c7b-253372f2cbc5"


@pytest.fixture
def results() -> RetrofitPlannerResponsePublic:
    with open(PATH_DATA / "a0ce4c08-6ca3-46f9-8c7b-253372f2cbc5.json") as file:
        return RetrofitPlannerResponsePublic.model_validate_json(file.read())


@pytest.fixture
def api_client() -> APIClient:
    """Return a DRF API client instance."""
    return APIClient()
