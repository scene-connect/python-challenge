"""
Helper functions.

These abstract away APIs or database interactions
which would normally exist in a real application.
"""
from pathlib import Path

PATH_DATA = Path(__file__).parent.parent / "data"


def get_home(uprn: str) -> Home:  # pragma: no cover
    if uprn == "906205784":
        with open(PATH_DATA / "906205784.json") as file:
            return Home.model_validate_json(file.read())
    raise ValueError("UPRN not found")


def get_results(uuid: str) -> RetrofitPlannerResponsePublic:  # pragma: no cover
    if uuid == "a0ce4c08-6ca3-46f9-8c7b-253372f2cbc5":
        with open(PATH_DATA / "a0ce4c08-6ca3-46f9-8c7b-253372f2cbc5.json") as file:
            return RetrofitPlannerResponsePublic.model_validate_json(file.read())
    raise ValueError("UUID not found")


# TODO could make both of these into django models and have a migration script to
#      pre-populate the database, but really who cares...
