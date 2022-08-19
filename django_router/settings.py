from dataclasses import dataclass

from django.conf import settings


@dataclass
class RouterSettings:
    NAME_WORDS_SEPARATOR: str = "_"
    TRY_USE_MODEL_NAMES: bool = True
    MODEL_NAMES_MONOLITHIC: bool = True


def get_settings():
    _settings = RouterSettings()
    project_settings = getattr(settings, "ROUTER_SETTINGS", {})
    intersection = project_settings.keys() & _settings.__dict__
    intersection
    for key in intersection:
        setattr(_settings, key, project_settings[key])
    return _settings


ROUTER_SETTINGS = get_settings()
