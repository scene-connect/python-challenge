import http

import pydantic_core
from django.urls import reverse
from pydantic import ValidationError
from pytest_mock import MockerFixture
from rest_framework.test import APIClient

from python_challenge.api.types import HomeDetailsResponse
from python_challenge.types.home import Home


def test_get_uprn(home: Home, uprn: str, mocker: MockerFixture, api_client: APIClient):
    mock_get_home = mocker.patch(
        "python_challenge.api.views.get_home", return_value=home
    )

    response = api_client.get(
        reverse("get-home", kwargs={"uprn": uprn}),
    )
    assert response.status_code == http.HTTPStatus.OK
    actual_response = HomeDetailsResponse.model_validate_json(response.content)
    assert actual_response.home == home
    mock_get_home.assert_called_once_with(uprn)


def test_get_unknown_uprn(uprn: str, mocker: MockerFixture, api_client: APIClient):
    mock_get_home = mocker.patch(
        "python_challenge.api.views.get_home",
        side_effect=FileNotFoundError("Couldn't find the file"),
    )

    response = api_client.get(
        reverse("get-home", kwargs={"uprn": uprn}),
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    mock_get_home.assert_called_once_with(uprn)


def test_get_invalid_data(uprn: str, mocker: MockerFixture, api_client: APIClient):
    mock_get_home = mocker.patch(
        "python_challenge.api.views.get_home",
        side_effect=ValidationError.from_exception_data(
            "some value is missing",
            [pydantic_core.InitErrorDetails(type="missing", input="input data")],
        ),
    )

    response = api_client.get(
        reverse("get-home", kwargs={"uprn": uprn}),
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    mock_get_home.assert_called_once_with(uprn)
