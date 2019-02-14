from decimal import Decimal

from django.test import TestCase

from places.models import Place, Room, Price, GeoName
from traveller.models import User, PlaceAccount


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

    def test_place_admin_list(self):
        User.objects.create(email='a@b.com')
        user = User.objects.create(email='a@c.com')
        self.assertEqual(2, user.id)
        Place.objects.create(name='test')
        place = Place.objects.create(name='test')
        PlaceAccount.objects.create(place_id=place.id, user_id=user.id)
        self.assertListEqual([2], place.admin_id_list)
        user = User.objects.create(email='b@b.com')
        self.assertListEqual([2], place.admin_id_list)
        PlaceAccount.objects.create(place_id=place.id, user_id=user.id)
        self.assertListEqual([2, 3], place.admin_id_list)

    def test_distance(self):
        place: Place = Place.objects.create(name='Lang', latitude=12, longitude=48.5)
        self.assertAlmostEqual(place.distance(latitude=11, longitude=48), 1.118, places=2)

    def test_categories_tiny(self):
        place: Place = Place.objects.create(name='Tiny')
        self.assertTrue(place.add_std_rooms_and_prices(std_price=Decimal(12.6), category=Place.TINY))
        self.assertEqual(1, place.room_set.count())
        self.assertEqual(2, place.beds)
        self.assertAlmostEqual(Decimal(12.6), place.room_set.first().price_per_person, 2)

    def test_categories_small(self):
        place: Place = Place.objects.create(name='Tiny')
        self.assertTrue(place.add_std_rooms_and_prices(std_price=Decimal(12.6), category=Place.SMALL))
        self.assertEqual(2, place.room_set.count())
        self.assertEqual(5, place.beds)

    def test_categories_medium(self):
        place: Place = Place.objects.create(name='Tiny')
        self.assertTrue(place.add_std_rooms_and_prices(std_price=Decimal(12.6), category=Place.MEDIUM))
        self.assertEqual(3, place.room_set.count())
        self.assertEqual(11, place.beds)

    def test_categories_large(self):
        place: Place = Place.objects.create(name='Tiny')
        self.assertTrue(place.add_std_rooms_and_prices(std_price=Decimal(12.6), category=Place.LARGE))
        self.assertEqual(4, place.room_set.count())
        self.assertEqual(14, place.beds)

    def test_email(self):
        place = Place.objects.create(name='test')
        user = User.objects.create(screen_name='mail user', email='a@b.de')
        PlaceAccount.objects.create(place_id=place.id, user_id=user.id)
        self.assertEqual('a@b.de', place.email)
        user2 = User.objects.create(screen_name='2nd mail user', email='b@b.de')
        PlaceAccount.objects.create(place_id=place.id, user_id=user2.id)
        self.assertEqual('a@b.de', place.email)  # sort by creation date, means id

    def test_price_repr(self):
        place = Place.objects.create(name='test')
        price = Price.objects.create(place_id=place.id)
        self.assertEqual('test () - CL - 0.0EUR', str(price))

    def test_geo_name_repr(self):
        GeoName.objects.create(name='Home', ascii_name='Home', country_code='DE', geo_name_id=1,
                               latitude=48.96, longitude=9.064)
        self.assertEqual('Home (DE):1', str(GeoName.objects.filter(pk=1).first()))

    def test_description(self):
        place = Place.objects.create(name='test', description='yeah')
        self.assertEqual('yeah', place.generated_description)

    def test_pets(self):
        place = Place.objects.create(name='test')
        room = Room.objects.create(price_per_person=12.5, room_number='01', pets=True, place_id=place.id)
        self.assertEqual(True, place.pets)
