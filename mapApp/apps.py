from django.apps import AppConfig

class MapAppConfig(AppConfig):
    name = 'mapApp'
    verbose_name = "Map App"

    def ready(self):
        import mapApp.signals
