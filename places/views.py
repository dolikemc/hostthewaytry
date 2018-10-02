from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Places


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Places.objects.order_by('-latitude')


class DetailView(generic.DetailView):
    template_name = 'places/detail.html'
    context_object_name = 'place'
    model = Places


def base_layout(request: HttpRequest) -> HttpResponse:
    template = 'places/w3base.html'
    return render(request, template)


# todo: picture send through this view
class CreatePlace(generic.CreateView):
    model = Places
    template_name = 'places/create_place.html'
    # todo: reduce fields and unit test still runs
    # fields = ['name', 'picture', 'country']
    fields = '__all__'
    user = User(is_staff=True)

    @login_required
    def dispatch(self, *args, **kwargs):
        return super(CreatePlace, self).dispatch(*args, **kwargs)

    # todo: use special save image file functionality
    # todo: split fields into optional and mandatory, eventually two screens (create and update)

    def post(self, request: HttpRequest, *args, **kwargs):
        print(request.body)
        return super(CreatePlace, self).post(request, *args, **kwargs)
