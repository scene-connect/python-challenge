"""Root URL Configuration."""

from django.shortcuts import redirect
from django.urls import include
from django.urls import path

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("docs/", include("python_challenge.docs.urls")),
    path("api/", include("python_challenge.api.urls")),
    path("", lambda x: redirect("/docs/")),
]
