import re

from django.views import generic

from django_router.settings import ROUTER_SETTINGS

CAMEL_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


def from_camel(string: str, separator=ROUTER_SETTINGS.NAME_WORDS_SEPARATOR):
    return CAMEL_PATTERN.sub(separator, string).lower()


DJANGO_ROUTER_MAP = {
    generic.ListView: ("list", ""),
    generic.CreateView: ("create", "create/"),
    generic.DetailView: ("detail", ""),
    generic.UpdateView: ("update", "update/"),
    generic.DeleteView: ("delete", "delete/"),
}

DJANGO_ADMIN_LIKE_MAP = {
    generic.ListView: ("changelist", ""),
    generic.CreateView: ("add", "add/"),
    generic.DetailView: ("detail", ""),
    generic.UpdateView: ("change", "change/"),
    generic.DeleteView: ("delete", "delete/"),
}
