from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
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


class CreatePlace(ModelForm):
    class Meta:
        model = Places
        # template_name = 'places/create_place.html'
        # todo: reduce fields and unit test still runs
        exclude = ['longitude', 'latitude', 'area']
        # fields = '__all__'
        # initial = {'name': 'Name', 'country': 'DE'}
        # user = User(is_staff=True)

    # todo: split fields into optional and mandatory, eventually two screens (create and update)


@login_required
def create_new_place(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        print(request.POST, request.FILES)
        form = CreatePlace(request.POST, request.FILES)
    else:
        form = CreatePlace()
    if form.is_valid():
        place = form.save()
        return redirect('places:detail', pk=place.pk)
    return render(request, 'places/create_place.html', {'form': form})
