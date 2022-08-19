import re

from django.views import generic

from django_router.settings import ROUTER_SETTINGS

CAMEL_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


def from_camel(string: str, separator=ROUTER_SETTINGS.NAME_WORDS_SEPARATOR):
    return CAMEL_PATTERN.sub(separator, string).lower()


VIEW_NAME_MAP = {
    generic.ListView: "list",
    generic.CreateView: "create",
    generic.DetailView: "detail",
    generic.UpdateView: "update",
    generic.DeleteView: "delete",
}
