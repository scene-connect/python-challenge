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
    return "1e0e7511-9e40-4b13-8c52-4f9c26c41c55"


@pytest.fixture
def results() -> RetrofitPlannerResponsePublic:
    with open(PATH_DATA / "1e0e7511-9e40-4b13-8c52-4f9c26c41c55.json") as file:
        return RetrofitPlannerResponsePublic.model_validate_json(file.read())


@pytest.fixture
def api_client() -> APIClient:
    """Return a DRF API client instance."""
    return APIClient()
