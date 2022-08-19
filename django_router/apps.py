from django.apps import AppConfig


class DjangoRouterConfig(AppConfig):
    name = "django_router"

    def ready(self):
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("views")
