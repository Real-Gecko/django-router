from django.db.models import Model
from django.urls import path, re_path

from django_router.settings import ROUTER_SETTINGS
from django_router.utils import VIEW_NAME_MAP, from_camel


class Router:
    def __init__(self):
        self._namespaces = dict()

    def path(self, pattern=None, name=None, **kwargs):
        def _wrapper(view):
            self._push(path, pattern, view, name, kwargs)
            return view

        return _wrapper

    def re_path(self, pattern, name=None, **kwargs):
        def _wrapper(view):
            self._push(re_path, pattern, view, name, kwargs)
            return view

        return _wrapper

    def _push(self, func, pattern, view, name, kwargs):
        namespace = view.__module__.split(".")[0]
        self._namespaces.setdefault(namespace, []).append(
            (func, pattern, view, name, kwargs)
        )

    @property
    def urlpatterns(self):
        urlpatterns = []
        for namespace, patterns in self._namespaces.items():
            paths = []
            for (func, pattern, view, name, kwargs) in patterns:

                if pattern is None:
                    pattern = from_camel(view.__name__) + "/"

                pattern = "/".join(view.__module__.split(".")[1:-1] + [pattern])

                if not name:
                    name_suffix = ""
                    model = getattr(view, "model", None)
                    if (
                        model
                        and isinstance(view, type)
                        and ROUTER_SETTINGS.TRY_USE_MODEL_NAMES
                        and issubclass(model, Model)
                    ):
                        if ROUTER_SETTINGS.MODEL_NAMES_MONOLITHIC:
                            name = model._meta.model_name
                        else:
                            name = from_camel(model._meta.object_name)
                        for key in VIEW_NAME_MAP:
                            if issubclass(view, key):
                                name_suffix = VIEW_NAME_MAP[key]
                            if not name_suffix:
                                name_suffix = from_camel(view.__name__)
                        name = name + ROUTER_SETTINGS.NAME_WORDS_SEPARATOR + name_suffix
                    else:
                        name = from_camel(view.__name__)

                if isinstance(view, type):
                    view = view.as_view()
                else:
                    view = view

                kwargs.update(name=name)

                paths.append(func(pattern, view, **kwargs))

            urlpatterns.append(path(f"{namespace}/", (paths, namespace, namespace)))

        return urlpatterns


router = Router()
