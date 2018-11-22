# import the logging library
import logging

# django modules
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.shortcuts import reverse
from django.views import generic

# my models
from places.models import Place, Price, Room

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    model = Place
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.filter(deleted__exact=False,
                                    reviewed__exact=True
                                    ).order_by('-latitude')


class DeletePrice(LoginRequiredMixin, generic.DeleteView):
    model = Price

    def get_success_url(self):
        return reverse('places:update-place', kwargs={'pk': self.object.place.id})

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class EditPrice(LoginRequiredMixin, generic.UpdateView):
    template_name = 'places/create_detail.html'
    context_object_name = 'form'
    model = Price
    fields = ['category', 'value', 'description', ]

    # pk_url_kwarg = 'place_id', , 'reviewed', 'deleted'

    def get_success_url(self):
        return reverse('places:update-place', kwargs={'pk': self.object.place.id})


class DeleteRoom(LoginRequiredMixin, generic.DeleteView):
    model = Room

    def get_success_url(self):
        return reverse('places:update-place', kwargs={'pk': self.object.place.id})

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class EditRoom(LoginRequiredMixin, generic.UpdateView):
    template_name = 'places/create_detail.html'
    context_object_name = 'form'
    model = Room
    fields = ['room_number', 'beds', 'bathroom', 'kitchen', 'outdoor_place', 'room_add', 'smoking', 'pets', 'family',
              'handicapped_enabled', 'price_per_person', 'price_per_room', ]
    localized_fields = ['valid_from', 'valid_to']

    def get_success_url(self):
        return reverse('places:update-place', kwargs={'pk': self.object.place.id})


class EditPlaceView(LoginRequiredMixin, ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        # todo: to clean
        return cleaned_data

    class Meta:
        model = Place
        fields = ['name', 'contact_type', 'website', 'languages', 'who_lives_here', 'currency',
                  'picture', 'description', 'outdoor_place', 'wifi', 'separate_entrance', 'common_kitchen',
                  'pick_up_service', 'parking', 'own_key', 'laundry', 'meals', 'meal_example',
                  'vegan', 'vegetarian', 'check_in_time', 'check_out_time']


class EditPlaceAddressView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'places/create_detail.html'
    context_object_name = 'form'
    model = Place
    fields = ['name', 'street', 'country', 'city', 'address_add', 'mobile', 'phone']

    def get_success_url(self):
        return reverse('places:detail', kwargs={'pk': self.object.id})


class DetailView(generic.DetailView):
    template_name = 'places/detail.html'
    context_object_name = 'place'
    model = Place


class NewPlaceMinimal(LoginRequiredMixin, ModelForm):
    """form for the minimum of information creating a new place"""
    breakfast_included = forms.BooleanField(initial=True)
    std_price = forms.DecimalField(decimal_places=2, label="Standard price for one night and one person")

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['country'] = str.upper(self.cleaned_data.get('country', ''))
        logger.debug(cleaned_data)
        return cleaned_data

    class Meta:
        model = Place
        fields = ['name', 'picture', 'description', 'laundry', 'parking',
                  'wifi', 'own_key', 'separate_entrance', 'category', 'country']


class AddPriceToPlace(LoginRequiredMixin, ModelForm):
    """add a price entry to the given place, therefore the place refernce is excluded"""
    required_css_class = 'w3-amber w3-input'

    class Meta:
        model = Price
        exclude = ['place']


class AddRoomToPlace(LoginRequiredMixin, ModelForm):
    class Meta:
        model = Room
        exclude = ['place']
        localized_fields = ['valid_from', 'valid_to']
