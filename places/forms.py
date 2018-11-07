# import the logging library
import logging

# django modules
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import reverse
from django.views import generic

# my models
from .models import Place, Price, Room

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class ReviewList(generic.ListView):
    context_object_name = 'places'

    def get_queryset(self):
        return Place.objects.filter(reviewed__exact=0).order_by('created_on')


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.order_by('-latitude')


class DeletePrice(generic.DeleteView):
    model = Price

    def get_success_url(self):
        return reverse('update-place', kwargs={'pk': self.object.place.id})

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class EditPrice(generic.UpdateView):
    template_name = 'places/create_detail.html'
    context_object_name = 'form'
    model = Price
    fields = ['category', 'value', 'description', ]

    # pk_url_kwarg = 'place_id', , 'reviewed', 'deleted'

    def get_success_url(self):
        return reverse('update-place', kwargs={'pk': self.object.place.id})


class DeleteRoom(generic.DeleteView):
    model = Room

    def get_success_url(self):
        return reverse('update-place', kwargs={'pk': self.object.place.id})

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class EditRoom(generic.UpdateView):
    template_name = 'places/create_detail.html'
    context_object_name = 'form'
    model = Room
    fields = ['room_number', 'beds', 'bathroom', 'kitchen', 'outdoor_place', 'room_add', 'smoking', 'pets', 'family',
              'handicapped_enabled', 'price_per_person', 'price_per_room', ]
    localized_fields = ['valid_from', 'valid_to']

    def get_success_url(self):
        return reverse('update-place', kwargs={'pk': self.object.place.id})


class EditPlaceView(ModelForm):
    class Meta:
        model = Place
        fields = '__all__'


class DetailView(generic.DetailView):
    template_name = 'places/detail.html'
    context_object_name = 'place'
    model = Place


class NewPlaceMinimal(ModelForm):
    """form for the minimum of information creating a new place"""
    breakfast_included = forms.BooleanField(initial=True)
    std_price = forms.DecimalField(decimal_places=2, label="Standard price for one night and one person")

    class Meta:
        model = Place
        fields = ['name', 'picture', 'description', 'laundry', 'parking',
                  'wifi', 'own_key', 'separate_entrance', 'category', 'country']
        # user = User()


class AddUser(ModelForm):
    """add an administrator to a place"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class EditPlace(ModelForm):
    """edit and create standard class for a place"""

    class Meta:
        model = Place
        exclude = ['longitude', 'latitude']
        # user = User(is_staff=True)


class AddPriceToPlace(ModelForm):
    """add a price entry to the given place, therefore the place refernce is excluded"""
    required_css_class = 'w3-amber w3-input'

    class Meta:
        model = Price
        exclude = ['place']


class AddRoomToPlace(ModelForm):
    class Meta:
        model = Room
        exclude = ['place']
        localized_fields = ['valid_from', 'valid_to']
