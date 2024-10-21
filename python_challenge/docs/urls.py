from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerSplitView

urlpatterns = [
    path("", SpectacularSwaggerSplitView.as_view(url_name="schema"), name="docs"),
    path("schema", SpectacularAPIView.as_view(), name="schema"),
]
