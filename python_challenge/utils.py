"""
Helper functions.

These abstract away APIs or database interactions
which would normally exist in a real application.
"""

from pathlib import Path

from .types.home import Home
from .types.retrofit_planner import RetrofitPlannerResponsePublic

PATH_DATA = Path(__file__).parent.parent / "data"


def get_home(uprn: str) -> Home:  # pragma: no cover
    if uprn == "906205784":
        with open(PATH_DATA / "906205784.json") as file:
            return Home.model_validate_json(file.read())
    raise FileNotFoundError("UPRN not found")


def get_results(uuid: str) -> RetrofitPlannerResponsePublic:  # pragma: no cover
    if uuid == "1e0e7511-9e40-4b13-8c52-4f9c26c41c55":
        with open(PATH_DATA / "1e0e7511-9e40-4b13-8c52-4f9c26c41c55.json") as file:
            return RetrofitPlannerResponsePublic.model_validate_json(file.read())
    raise FileNotFoundError("UUID not found")


# TODO could make both of these into django models and have a migration script to
#      pre-populate the database, but really who cares...
