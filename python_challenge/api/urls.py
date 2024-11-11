from django.urls import path

from . import views

urlpatterns = [
    # Legacy URLs, to be deprecated in v5 ?
    path(
        r"home/<str:uprn>",
        views.HomeDetailsByUPRN.as_view(),
        name="get-home",
    ),
    path(
        r"before_after_energy_usage/<str:uuid>",
        views.EnergyComparisonByUUID.as_view(),
        ),
]
