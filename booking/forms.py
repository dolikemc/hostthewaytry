# import the logging library
import logging

# django modules
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import generic

# my models
from booking.models import Booking
from places.models import Place

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class BookingCreate(generic.CreateView):
    # login_url = '/traveller/login/'
    model = Booking
    fields = '__all__'
    template_name = 'booking/create.html'

    def get_success_url(self):
        return reverse('places:detail', kwargs={'pk': self.get_place_id()})

    def form_valid(self, form):
        new_model = form.save(commit=False)
        new_model.place = Place.objects.get(id=self.get_place_id())
        new_model.user = self.request.user
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return True

    def get_place_id(self):
        for key in ('pk', 'place', 'place_id', 'id'):
            if key in self.kwargs:
                logger.debug(f'Place id from {key} parameter is {self.kwargs[key]}')
                return self.kwargs[key]
        return 0
