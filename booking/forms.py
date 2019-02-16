# import the logging library
import logging
from datetime import date, timedelta

# django modules
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import generic

from booking.models import Booking
# my models
from places.models import Place

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class BookingEmail(forms.Form):
    other_email = forms.EmailField(widget=forms.EmailInput)
    place_email = forms.EmailField(disabled=True)
    date_from = forms.DateField(widget=forms.SelectDateWidget)
    date_to = forms.DateField(widget=forms.SelectDateWidget)
    adults = forms.IntegerField(widget=forms.NumberInput)
    kids = forms.IntegerField(widget=forms.NumberInput)
    message = forms.CharField(widget=forms.Textarea, required=False)


class BookingCreate(LoginRequiredMixin, generic.edit.FormMixin, generic.DetailView):
    login_url = '/traveller/login/'
    form_class = BookingEmail
    model = Place
    template_name = 'booking/create.html'

    def get_success_url(self):
        return reverse('places:detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        logger.debug(self.request.POST)
        self.object = self.get_object()
        Booking.objects.create(place=self.object,
                               traveller=self.request.user,
                               adults=form.cleaned_data['adults'],
                               kids=form.cleaned_data['kids'],
                               date_from=form.cleaned_data['date_from'],
                               date_to=form.cleaned_data['date_to'],
                               message=form.cleaned_data['message'])
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        self.object = self.get_object()
        return {'place_email': self.object.email,
                'other_email': self.request.user.email,
                'date_from': date.today(),
                'date_to': date.today() + timedelta(days=1),
                'adults': 2,
                'kids': 0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
