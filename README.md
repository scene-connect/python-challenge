# Scene coding challenge
A technical interview challenge for python developers.

This live-coding challenge is as much about demonstrating the process as it is about the
end-result.

## Getting started
You will need:
- git
- python (^3.11)
- poetry (`pipx install poetry` is easiest)

You should be able to clone this repository, and setup a virtual environment using
poetry:
```shell
poetry install
poetry shell
```

Copy the example environment file:
```shell
cp .env.example .env
```

### Running the Django server

From a shell within the poetry virtual environment:
```shell
python manage.py runserver
```

You can access the documentation at: [http://localhost:8000/docs/](http://localhost:8000/docs/)

The basic `api` Django app does not use authentication. You can try out the existing
`/api/home/{uprn}` endpoint with UPRN: `906205784`. This will return a
`HomeDetailsResponse` object with details of the property.

For the challenge we're not actually using a database, so the APIs will only fetch
hard-coded data. No other UPRNs will work with this endpoint.


## Challenge

1. Add a simple "UI" prototype for a chart, comparing monthly energy usage before and
after a set of home improvements.
    - Use the tools you think get you the best results the quickest.
        - This could be a single-page-application framework, or just HTML with a
          [Django view](https://docs.djangoproject.com/en/5.1/topics/http/views/)
          using CDN assets.
        - If you do not have a preferred JavaScript charting library, try
          [ChartJS](https://www.chartjs.org/).
    - You can choose whatever chart style you feel is most appropriate.
    - You don't need to consider aesthetics, just make the chart understandable.
    - You do not need to consider security, access controls, or other usual best-practices
      for this challenge. Treat it as an internal prototyping exercise.

2. You should add an endpoint to the `python_challenge.api.views` to supply the data for
   the chart.
    - We have provided a utility function `python_challenge.utils.get_results` which
      fetches a `RetrofitPlannerResponsePublic` object.
        - This object contains all the data you will need (and more, see the notes below
          about what data to use).
        - You can use the UUID `1e0e7511-9e40-4b13-8c52-4f9c26c41c55` which has baseline
          and improved simulation results for UPRN `906205784`.
    - You should format the data into whatever structure your chart requires, in python.


### RetrofitPlannerResponsePublic

The `RetrofitPlannerResponsePublic` has a lot of data, but for this challenge the two
fields you need are:
- `$.baseline_energy_profile.monthly_energy_total`
- `$.improvement_plan.energy_profile.monthly_energy_total`

These are both `dict[MonthNumber, EnergyConsumptionSummary]`, and have an `energy`
sub-field with the total household energy consumption for the month, in kWh.

The chart needs to compare these two data series. You should choose how best to display
the data.


## Notes

### `python_challenge/types/`

Do not change or add any code to `python_challenge/types/`.
This is a collection of type definitions copied over from one of our packages.
Treat it as an external dependency.

### Linting

We have included several python linter tools we use: black, isort, ruff, pyright.
These are configured to be run with [pre-commit](https://pre-commit.com/) and will be
run before each commit and push.

Please install and check the pre-commit hooks with:
```shell
pre-commit install
pre-commit run --all-files
```

- We have a 100% test-coverage policy, so please add a unit test to
`python_challenge/api/tests/` for the new endpoint.
    - Currently, test-coverage is not 100% because we have provided some fixtures for
    you to use in your test, see `python_challenge/api/tests/conftest.py`
    - For the UI prototype you do not need to write equivalent unit tests, however
      if you do add the UI as a Django view please add a test to check that the view
      responds with a `HTTPStatus.OK`
