from decimal import Decimal

from django.test import TestCase
from django.test.utils import skipIf

from places.models import Place, Room


class PlaceModel(TestCase):
    def test_properties(self):
        place = Place.objects.create(name='test')
        room = Room.objects.create(price_per_person=12.5, room_number='01', beds=2, place_id=place.id)
        place.room_set.add(room)
        room2 = Room.objects.create(price_per_person=13.5, room_number='02', beds=3, place_id=place.id)
        place.room_set.add(room2)
        self.assertEqual(place.average_price, Decimal(13.0))
        self.assertEqual(place.bathrooms, 2)
        self.assertTrue(place.private_bathroom)
        self.assertFalse(place.smoking)
        self.assertEqual(place.beds, 5)

    def test_distance(self):
        place: Place = Place.objects.create(name='Lang', latitude=12, longitude=48.5)
        self.assertAlmostEqual(place.distance(latitude=11, longitude=48), 1.118, places=2)

    @skipIf(True, 'not yet implemented')
    def test_categories(self):
        pass
