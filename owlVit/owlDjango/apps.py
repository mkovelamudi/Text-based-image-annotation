from django.apps import AppConfig
from .model import loadModel


class OwldjangoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "owlDjango"

    def ready(self) -> None:
        loadModel.load_model()

