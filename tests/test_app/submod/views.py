from django.views.generic import View

from django_router import router


@router.path("")
class SubIndexView(View):
    pass
