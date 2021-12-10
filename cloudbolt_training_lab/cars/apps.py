from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CarsConfig(AppConfig):
    name = "cars"
    verbose_name = _("Cars")

    def ready(self):
        try:
            import cloudbolt_training_lab.cars.signals  # noqa F401
        except ImportError:
            pass
