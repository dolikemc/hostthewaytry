from datetime import date

from django.http.response import HttpResponse
from django.shortcuts import reverse

from booking.models import Booking
from places.models import Place
from tests.base import BaseTest


class BookingViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.last_place_id = Place.objects.create(name='Test').id

    def test_open_booking(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response: HttpResponse = self.client.get(reverse('booking:create-booking', kwargs={'pk': self.last_place_id}))
        self.assertContains(response, 'test@user.com')

    def test_add_booking(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        place = Place.objects.get(pk=self.last_place_id)
        response: HttpResponse = self.client.post(reverse('booking:create-booking',
                                                          kwargs={'pk': self.last_place_id}),
                                                  data={'message': 'hallo',
                                                        'date_from': date(2019, 1, 1),
                                                        'date_to': date(2019, 1, 2),
                                                        'adults': 2, 'kids': 0,
                                                        'place': place.id,
                                                        'traveller': self.user.id
                                                        }
                                                  )
        self.assertRedirects(response, reverse('places:detail',
                                               kwargs={'pk': place.id}))
        self.assertEqual(1, Booking.objects.count())
        booking = Booking.objects.get(pk=1)
        self.assertIsInstance(booking, Booking)
        self.assertEqual(self.last_place_id, booking.place.id)
