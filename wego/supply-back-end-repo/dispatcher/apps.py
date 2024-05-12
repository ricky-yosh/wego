from django.apps import AppConfig


class DispatcherConfig(AppConfig):
    name = 'dispatcher'

    def ready(self):
        from .tasks import start_scheduler
        start_scheduler()

