from datetime import date, timedelta

from django.test import TestCase

from booking.models import Booking
from places.models import Place
from traveller.models import User


class BookingModel(TestCase):
    def test_creation(self):
        user = User.objects.create(email='a@b.com', screen_name='traveller', unique_name='traveller')
        place = Place.objects.create(name='Test', country='DE')
        booking = Booking.objects.create(place=place, traveller=user, date_from=date.today(), adults=2,
                                         date_to=date.today() + timedelta(days=1))
        self.assertTrue(booking)
        self.assertEqual('1: traveller@Test (DE)', str(booking))
        self.assertEqual(2, booking.adults)
        self.assertEqual(0, booking.kids)
        self.assertEqual(date.today(), booking.date_from)
