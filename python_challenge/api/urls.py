from django.urls import path

from . import views
from . import PythonChallenge

urlpatterns = [
    # Legacy URLs, to be deprecated in v5 ?
    path(
        r"home/<str:uprn>",
        views.HomeDetailsByUPRN.as_view(),
        name="get-home",
    ),
    path(
        r"python-chaalenge/<str:uuid>",
        PythonChallenge.PythonChallenge.as_view(),
        name="get-new",
    ),
]
