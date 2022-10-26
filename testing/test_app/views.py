from django.views import generic
from test_app import models

from django_router import router


@router.path()
def simple_fbv(test):
    pass


@router.path()
class SimpleCbv(generic.View):
    pass


@router.path()
class ListSome(generic.ListView):
    model = models.ModelName


@router.path()
class CreateSome(generic.CreateView):
    model = models.ModelName


@router.path()
class JustADetailView(generic.DetailView):
    model = models.ModelName


@router.path()
class LetsUpdate(generic.UpdateView):
    model = models.ModelName


@router.path()
class RemoveIt(generic.DeleteView):
    model = models.ModelName


@router.path()
class DoSomething(generic.View):
    model = models.ModelName


@router.re_path(r"^index/$")
def index(request):
    pass
