from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class RouterSettings:
    SIMPLE_AUTO_NAMING: bool = False
    WORDS_SEPARATOR: str = "_"
    MODEL_NAMES_MONOLITHIC: bool = True
    ADMIN_LIKE_VERBS: bool = False
    MODULE_PATH_MAP: bool = True

    def __init__(self):
        project_settings = getattr(settings, "ROUTER_SETTINGS", {})
        if "NAME_WORDS_SEPARATOR" in project_settings:  # pragma: no cover
            raise ImproperlyConfigured(
                "Option NAME_WORDS_SEPARATOR for Django Router renamed to WORDS_SEPARATOR"
            )
        if "DJANGO_ADMIN_LIKE_NAMES" in project_settings:  # pragma: no cover
            raise ImproperlyConfigured(
                "Option DJANGO_ADMIN_LIKE_NAMES for Django Router renamed to ADMIN_LIKE_VERBS"
            )
        if "TRY_USE_MODEL_NAMES" in project_settings:  # pragma: no cover
            raise ImproperlyConfigured(
                "Option TRY_USE_MODEL_NAMES for Django router is deprecated"
            )

    def __getattribute__(self, name):
        project_settings = getattr(settings, "ROUTER_SETTINGS", {})
        return project_settings.get(name, super().__getattribute__(name))


ROUTER_SETTINGS = RouterSettings()
