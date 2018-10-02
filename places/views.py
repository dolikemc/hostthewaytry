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


class CreatePlace(generic.CreateView):
    model = Places
    template_name = 'places/create_place.html'
    fields = '__all__'
