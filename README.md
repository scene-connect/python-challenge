# Scene coding challenge
A technical interview challenge for python developers.

This live-coding challenge is as much about demonstrating the process as it is about the
end-result.

## Getting started
You will need:
- git
- python (^3.11)
- poetry (^2.1)
  - Install with `pipx install "poetry>=2.1"`
  - And install the `poetry-shell` plugin for easier virtual environments: `pipx inject poetry poetry-plugin-shell`
  - Or see [their installation instructions](https://python-poetry.org/docs/#installation)

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

---

## Challenge

### User story
Home owners need a chart to compare the current (baseline) energy usage of their home
(from our simulations) and the potential _improved_ energy usage with proposed energy
saving measures.

This challenge is to create a prototype for that chart.

### Technical requirements

You should choose the best chart style to display the data.

You do not need to consider security, access controls, or other usual best-practices
for this challenge. Treat it as an internal prototyping exercise.

There are two major components for the challenge:

1. API
    - You should add a new endpoint to the `python_challenge.api.views` to supply the
      data for the chart.
    - There is an existing Django view for getting a `Home` object, with the details of
      the home (by UPRN - Unique Property Reference Number). This is provided as an example
      in case you aren't familiar with Django (and Django Rest Framework).
    - You should add a second view, which will return the necessary chart data.
      - The data formatting should be done in python, so that the UI (above) simply
        gets the necessary data for the chart.
    - We have provided a utility function `python_challenge.utils.get_results` in `utils.py`
      which fetches a `RetrofitPlannerResponsePublic` object.
        - This object contains all the data you will need (and more, see the notes below
          about what data to use).
        - You can use the UUID `1e0e7511-9e40-4b13-8c52-4f9c26c41c55` which has baseline (before)
          and improved (after) energy results for a home.
      - Unit tests
        - We have a 100% code coverage target for all our python projects.
        - Please see the notes below.
    - You should format the data into whatever structure your chart requires in python.
2. Chart
    - Add a simple prototype for the chart
    - The chart needs to compare two sets of monthly energy data.
        - Pick the best chart style to display the data, but aesthetics are not a
          requirement for this prototype.
    - Use the tools you think get you the best results the quickest.
        - This could be a single-page-application framework, a simple HTML page, or a
          [Django view](https://docs.djangoproject.com/en/5.1/topics/http/views/)
        - You can use CDN assets for any libraries.
        - If you do not have a preferred JavaScript charting library, try
          [ChartJS](https://www.chartjs.org/).
    - You can choose whatever chart style you feel is most appropriate.
    - You don't need to consider aesthetics, just make the chart understandable.
    - You do not need to write any unit tests for the chart.

## Data structures
### RetrofitPlannerResponsePublic

The `RetrofitPlannerResponsePublic` has a lot of data, but for this challenge the two
fields you need are:
- `baseline_energy_profile.monthly_energy_total`
- `improvement_plan[0].energy_profile.monthly_energy_total`

These are both `dict[MonthNumber, EnergyConsumptionSummary]`, and have an `energy`
sub-field with the total household energy consumption for the month, in kWh.
They also include cost and carbon, but we don't need to display that data for this
prototype chart.

---
## Notes

### `python_challenge/types/`

Do not change or add any code to `python_challenge/types/`.
This is a collection of type definitions copied over from one of our packages.
Treat it as an external dependency.

### Linting

We have included several python linter tools we use: black, isort, ruff, pyright.
These are configured to be run with [pre-commit](https://pre-commit.com/) and will be
run before each commit and push.

Please install the git hooks once you have set up your virtual environment:
```shell
pre-commit install
```

The checks should run automatically before each commit and push, but you can also
run them manually with:
```shell
pre-commit run --all-files
```

### Unit tests

You can run the existing tests with:
```shell
pytest
```
This will  also provide a coverage report.

We have provided some test fixtures for you to use in your test, see: `python_challenge/api/tests/conftest.py`

For the UI prototype you do not need to write equivalent unit tests, however
if you do add the UI as a Django view please add a test to check that the view
responds to requests with a `HTTPStatus.OK`.
