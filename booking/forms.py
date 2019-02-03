# import the logging library
import logging
from datetime import date, timedelta

# django modules
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import modelform_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import generic

# my models
from booking.models import Booking
from places.models import Place

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class BookingCreate(LoginRequiredMixin, generic.CreateView):
    login_url = '/traveller/login/'
    context_object_name = 'form'
    form_class = modelform_factory(Booking,
                                   widgets={'date_from': forms.widgets.SelectDateWidget,
                                            'date_to': forms.widgets.SelectDateWidget,
                                            'adults': forms.widgets.NumberInput,
                                            'kids': forms.widgets.NumberInput,
                                            'other_email': forms.widgets.EmailInput},
                                   fields=['traveller', 'place',
                                           'date_from', 'date_to', 'adults', 'kids', 'message',
                                           ])

    template_name = 'booking/create.html'

    def get_success_url(self):
        return reverse('places:detail', kwargs={'pk': self.get_place_id()})

    def form_valid(self, form):
        logger.debug(self.request.POST)
        new_model = form.save(commit=False)
        new_model.place = Place.objects.get(id=self.get_place_id())
        new_model.user = self.request.user
        new_model.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return True

    def get_place_id(self):
        for key in ('pk', 'place', 'place_id', 'id'):
            if key in self.kwargs:
                logger.debug(f'Place id from {key} parameter is {self.kwargs[key]}')
                return self.kwargs[key]
        return 0

    def get_initial(self):
        return {'place': Place.objects.get(pk=self.get_place_id()),
                'traveller': self.request.user, 'date_from': date.today(),
                'date_to': date.today() + timedelta(days=1), 'adults': 2, 'kids': 0}
