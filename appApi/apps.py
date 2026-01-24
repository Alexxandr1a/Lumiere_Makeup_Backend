from django.apps import AppConfig


class AppapiConfig(AppConfig):
    name = 'appApi'

def ready(self):
    import appApi.signals