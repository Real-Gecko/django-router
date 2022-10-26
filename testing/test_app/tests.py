import json
import sys
from importlib import import_module, reload
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings


class DjangoRouterTestCaseMixin:
    test_matrix: dict

    def setUp(self):
        # We must reload `urls.py` for settings changes to take effect
        urlconf = settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
        else:
            import_module(urlconf)

    def test_urls(self):
        # Get URLs
        with StringIO() as buffer:
            call_command("show_urls", format="json", stdout=buffer)
            show_urls = json.loads(buffer.getvalue())

        urls = {}
        for url in show_urls:
            urls[url["module"]] = [url["url"], url["name"]]

        # Run tests
        for view in self.test_matrix:
            self.assertEqual(self.test_matrix[view], urls[view])

        # print(f"--- {self.__class__.__name__} ---")
        # print(urls)


class DefaultTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.ListSome": [
            "/test_app/modelname/",
            "test_app:modelname_list",
        ],
        "test_app.views.JustADetailView": [
            "/test_app/modelname/<int:pk>/",
            "test_app:modelname_detail",
        ],
        "test_app.views.RemoveIt": [
            "/test_app/modelname/<int:pk>/delete/",
            "test_app:modelname_delete",
        ],
        "test_app.views.LetsUpdate": [
            "/test_app/modelname/<int:pk>/update/",
            "test_app:modelname_update",
        ],
        "test_app.views.CreateSome": [
            "/test_app/modelname/create/",
            "test_app:modelname_create",
        ],
        "test_app.views.DoSomething": [
            "/test_app/modelname/do_something/",
            "test_app:modelname_do_something",
        ],
        "test_app.views.SimpleCbv": ["/test_app/simple_cbv/", "test_app:simple_cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


@override_settings(ROUTER_SETTINGS={"SIMPLE_AUTO_NAMING": True})
class SimpleNamingTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.CreateSome": ["/test_app/create_some/", "test_app:create_some"],
        "test_app.views.DoSomething": [
            "/test_app/do_something/",
            "test_app:do_something",
        ],
        "test_app.views.JustADetailView": [
            "/test_app/just_a_detail_view/",
            "test_app:just_a_detail_view",
        ],
        "test_app.views.LetsUpdate": ["/test_app/lets_update/", "test_app:lets_update"],
        "test_app.views.ListSome": ["/test_app/list_some/", "test_app:list_some"],
        "test_app.views.RemoveIt": ["/test_app/remove_it/", "test_app:remove_it"],
        "test_app.views.SimpleCbv": ["/test_app/simple_cbv/", "test_app:simple_cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


@override_settings(ROUTER_SETTINGS={"WORDS_SEPARATOR": "-"})
class WordsSeparatorTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.ListSome": [
            "/test_app/modelname/",
            "test_app:modelname-list",
        ],
        "test_app.views.JustADetailView": [
            "/test_app/modelname/<int:pk>/",
            "test_app:modelname-detail",
        ],
        "test_app.views.RemoveIt": [
            "/test_app/modelname/<int:pk>/delete/",
            "test_app:modelname-delete",
        ],
        "test_app.views.LetsUpdate": [
            "/test_app/modelname/<int:pk>/update/",
            "test_app:modelname-update",
        ],
        "test_app.views.CreateSome": [
            "/test_app/modelname/create/",
            "test_app:modelname-create",
        ],
        "test_app.views.DoSomething": [
            "/test_app/modelname/do-something/",
            "test_app:modelname-do-something",
        ],
        "test_app.views.SimpleCbv": ["/test_app/simple-cbv/", "test_app:simple-cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


@override_settings(ROUTER_SETTINGS={"TRY_USE_MODEL_NAMES": False})
class UseModelNamesTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.CreateSome": ["/test_app/create_some/", "test_app:create_some"],
        "test_app.views.JustADetailView": [
            "/test_app/just_a_detail_view/",
            "test_app:just_a_detail_view",
        ],
        "test_app.views.LetsUpdate": ["/test_app/lets_update/", "test_app:lets_update"],
        "test_app.views.ListSome": ["/test_app/list_some/", "test_app:list_some"],
        "test_app.views.RemoveIt": ["/test_app/remove_it/", "test_app:remove_it"],
        "test_app.views.SimpleCbv": ["/test_app/simple_cbv/", "test_app:simple_cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.DoSomething": [
            "/test_app/do_something/",
            "test_app:do_something",
        ],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


@override_settings(ROUTER_SETTINGS={"MODEL_NAMES_MONOLITHIC": False})
class ModelNamesMonolithicTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.ListSome": [
            "/test_app/model_name/",
            "test_app:model_name_list",
        ],
        "test_app.views.JustADetailView": [
            "/test_app/model_name/<int:pk>/",
            "test_app:model_name_detail",
        ],
        "test_app.views.RemoveIt": [
            "/test_app/model_name/<int:pk>/delete/",
            "test_app:model_name_delete",
        ],
        "test_app.views.LetsUpdate": [
            "/test_app/model_name/<int:pk>/update/",
            "test_app:model_name_update",
        ],
        "test_app.views.CreateSome": [
            "/test_app/model_name/create/",
            "test_app:model_name_create",
        ],
        "test_app.views.DoSomething": [
            "/test_app/model_name/do_something/",
            "test_app:model_name_do_something",
        ],
        "test_app.views.SimpleCbv": ["/test_app/simple_cbv/", "test_app:simple_cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


@override_settings(ROUTER_SETTINGS={"ADMIN_LIKE_VERBS": True})
class DjangoAdminLikeTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.ListSome": [
            "/test_app/modelname/",
            "test_app:modelname_changelist",
        ],
        "test_app.views.JustADetailView": [
            "/test_app/modelname/<int:pk>/",
            "test_app:modelname_detail",
        ],
        "test_app.views.LetsUpdate": [
            "/test_app/modelname/<int:pk>/change/",
            "test_app:modelname_change",
        ],
        "test_app.views.RemoveIt": [
            "/test_app/modelname/<int:pk>/delete/",
            "test_app:modelname_delete",
        ],
        "test_app.views.CreateSome": [
            "/test_app/modelname/add/",
            "test_app:modelname_add",
        ],
        "test_app.views.DoSomething": [
            "/test_app/modelname/do_something/",
            "test_app:modelname_do_something",
        ],
        "test_app.views.SimpleCbv": ["/test_app/simple_cbv/", "test_app:simple_cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


@override_settings(
    ROUTER_SETTINGS={
        "WORDS_SEPARATOR": "-",
        "MODEL_NAMES_MONOLITHIC": False,
    }
)
class SeparatorAndNamesTestCase(DjangoRouterTestCaseMixin, TestCase):
    test_matrix = {
        "test_app.views.ListSome": [
            "/test_app/model-name/",
            "test_app:model-name-list",
        ],
        "test_app.views.JustADetailView": [
            "/test_app/model-name/<int:pk>/",
            "test_app:model-name-detail",
        ],
        "test_app.views.RemoveIt": [
            "/test_app/model-name/<int:pk>/delete/",
            "test_app:model-name-delete",
        ],
        "test_app.views.LetsUpdate": [
            "/test_app/model-name/<int:pk>/update/",
            "test_app:model-name-update",
        ],
        "test_app.views.CreateSome": [
            "/test_app/model-name/create/",
            "test_app:model-name-create",
        ],
        "test_app.views.DoSomething": [
            "/test_app/model-name/do-something/",
            "test_app:model-name-do-something",
        ],
        "test_app.views.SimpleCbv": ["/test_app/simple-cbv/", "test_app:simple-cbv"],
        "test_app.views.simple_fbv": ["/test_app/simple_fbv/", "test_app:simple_fbv"],
        "test_app.views.index": ["/test_app/index/", "test_app:index"],
    }


class TestManagementCommands(TestCase):
    def test_commands(self):
        with StringIO() as buffer:
            call_command("router_urls", stdout=buffer)
            call_command("router_list", stdout=buffer)
