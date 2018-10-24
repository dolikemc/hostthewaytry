# import the logging library
import logging

# django modules
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.views import generic

# my models
from .models import Place, Price, Room

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.order_by('-latitude')


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
