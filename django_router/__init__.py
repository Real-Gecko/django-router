from django.db.models import Model
from django.urls import path, re_path
from django.views.generic import CreateView
from django.views.generic.detail import SingleObjectMixin

from django_router.settings import ROUTER_SETTINGS as settings
from django_router.utils import DJANGO_ADMIN_LIKE_MAP, DJANGO_ROUTER_MAP, from_camel


class Router:
    def __init__(self):
        self._namespaces = dict()
        if settings.DJANGO_ADMIN_LIKE_NAMES:
            self._parameter_map = DJANGO_ADMIN_LIKE_MAP
        else:
            self._parameter_map = DJANGO_ROUTER_MAP

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
                model = getattr(view, "model", None)
                model_name = ""
                if model:
                    if settings.MODEL_NAMES_MONOLITHIC:
                        model_name = model._meta.model_name
                    else:
                        model_name = from_camel(model._meta.object_name)
                if not name:
                    parameter_map = (
                        from_camel(view.__name__),
                        from_camel(view.__name__) + "/",
                    )
                    if (
                        model_name
                        and isinstance(view, type)
                        and settings.TRY_USE_MODEL_NAMES
                        and issubclass(model, Model)
                    ):
                        for key in self._parameter_map:
                            if issubclass(view, key):
                                parameter_map = self._parameter_map[key]
                                continue

                        name = settings.NAME_WORDS_SEPARATOR.join(
                            [model_name, parameter_map[0]]
                        )
                        if pattern is None:
                            to_join = [model_name]
                            if issubclass(view, SingleObjectMixin) and not issubclass(
                                view, CreateView
                            ):
                                to_join.append("<int:pk>")
                            to_join.append(parameter_map[1])
                            pattern = "/".join(to_join)
                    else:
                        name = from_camel(view.__name__)
                if pattern is None:
                    pattern = name + "/"

                pattern = "/".join(view.__module__.split(".")[1:-1] + [pattern])

                if isinstance(view, type):
                    view = view.as_view()
                else:
                    view = view

                kwargs.update(name=name)

                paths.append(func(pattern, view, **kwargs))

            urlpatterns.append(path(f"{namespace}/", (paths, namespace, namespace)))

        return urlpatterns


router = Router()
