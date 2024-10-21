from django.apps import AppConfig
from django.db.models import CharField
from django.db.models.functions import Length


class DocsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "python_challenge.docs"

    def ready(self):
        CharField.register_lookup(Length)
