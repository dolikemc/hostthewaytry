# import the logging library
import logging

# django moduls
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

# my models
from .models import Place, Price, Room

# Get an instance of a logger
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.order_by('-latitude')


# todo: load prices and room information to be displayed in the form
class DetailView(generic.DetailView):
    template_name = 'places/detail.html'
    context_object_name = 'place'
    model = Place


def base_layout(request: HttpRequest) -> HttpResponse:
    """ method to store base layout via service worker"""
    template = 'places/w3base.html'
    return render(request, template)


class EditPlace(ModelForm):
    """edit and create standard class for a place"""

    class Meta:
        model = Place
        exclude = ['longitude', 'latitude']
        # user = User(is_staff=True)


# todo: split fields into optional and mandatory, eventually two screens (create and update)


@login_required
def create_new_place(request: HttpRequest) -> HttpResponse:
    """create a new place"""
    if request.method == 'POST':
        logger.info(request.POST)
        logger.info(str(request.FILES))
        form = EditPlace(request.POST, request.FILES)
    else:
        form = EditPlace()
    if form.is_valid():
        place = form.save(commit=False)
        # make a few up shifts
        place.country = str.upper(place.country)
        place.languages = str.upper(place.languages)
        place.save()
        return redirect('places:detail', pk=place.pk)
    return render(request, 'places/create_place.html', {'form': form})


@login_required
def change_place(request: HttpRequest, pk: int) -> HttpResponse:
    """change a place using inline formset"""
    # todo: enhance change place inline formset
    place = Place.objects.get(pk=pk)
    place_inline_formset = inlineformset_factory(Place, Room, fields='__all__')
    if request.method == "POST":
        formset = place_inline_formset(request.POST, request.FILES, instance=place)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect('places:detail', pk=place.pk)
    else:
        formset = place_inline_formset(instance=place)
    return render(request, 'places/create_place.html', {'formset': formset})


# todo: use Styling required or erroneous form rows Form.error_css_class Form.required_css_class

class AddPriceToPlace(ModelForm):
    """add a price entry to the given place, therefore the place refernce is excluded"""
    required_css_class = 'w3-amber w3-input'

    class Meta:
        model = Price
        exclude = ['place']


@login_required
def create_new_price(request: HttpRequest, place: int) -> HttpResponse:
    """ new price added to a by id given place"""
    if request.method == 'POST':
        form = AddPriceToPlace(request.POST, request.FILES)
    else:
        form = AddPriceToPlace()

    if form.is_valid():
        logger.info(form.data)
        price = form.save(commit=False)
        price.place_id = place
        price.save()
        return redirect('places:detail', pk=price.place_id)
    return render(request, 'places/create_price.html', {'form': form})


class AddRoomToPlace(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        localized_fields = ['valid_from', 'valid_to']


@login_required
def create_new_room(request: HttpRequest, place: int) -> HttpResponse:
    if request.method == 'POST':
        form = AddRoomToPlace(request.POST, request.FILES)
    else:
        form = AddRoomToPlace()
        form.place_id = place
    if form.is_valid():
        room = form.save()
        return redirect('places:detail', pk=room.place_id)
    return render(request, 'places/create_room.html', {'form': form})


@login_required
def update_place(request: HttpRequest, pk: int) -> HttpResponse:
    room_form_set = modelformset_factory(model=Room, fields='__all__', max_num=1)
    price_form_set = modelformset_factory(model=Price, fields='__all__', max_num=3)
    place_form_set = modelformset_factory(model=Place, fields='__all__', max_num=1)
    if request.method == 'POST':
        room_form_set = room_form_set(request.POST, request.FILES,
                                      queryset=Room.objects.filter(place_id__exact=pk),
                                      prefix='room')
        price_form_set = price_form_set(request.POST, request.FILES,
                                        queryset=Price.objects.filter(place_id__exact=pk),
                                        prefix='price')
        place_form_set = place_form_set(request.POST, request.FILES, queryset=Place.objects.filter(id=pk), )
        if room_form_set.is_valid() and price_form_set.is_valid() and place_form_set.is_valid():
            # do something with the cleaned_data on the formsets.

            room_form_set.save()
            place = place_form_set.save()
            price_form_set.save()
            return redirect('places:detail', pk=pk)
    else:
        room_form_set = room_form_set(prefix='room', queryset=Room.objects.filter(place_id__exact=pk), )
        price_form_set = price_form_set(prefix='price', queryset=Price.objects.filter(place_id__exact=pk), )
        place_form_set = place_form_set(queryset=Place.objects.filter(id=pk), )

    return render(request, 'places/create_place.html', {
        'formset': price_form_set,
        'room_formset': room_form_set,
        'form': place_form_set,
    })
