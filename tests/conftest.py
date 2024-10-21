from pathlib import Path

import pytest

PATH_DATA = Path(__file__).parent / "data"

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
