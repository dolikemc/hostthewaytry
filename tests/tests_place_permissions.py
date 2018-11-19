from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from places.models import Place, Room


# noinspection PyArgumentList
class NewPlaceProcess(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        # todo: should not need stuff policies, just allowance to add places
        User.objects.create_user(**self.credentials, is_staff=True)

    def test_create_minimal_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        fp = SimpleUploadedFile(name='IMG_3745.JPG',
                                content=open('static/places/img/IMG_3745.JPG', 'rb').read(),
                                content_type='image/jpeg')
        response = self.client.post('/places/new/', data={'name': 'New place', 'picture': fp,
                                                          'category': 'NA', 'std_price': '12.20',
                                                          'breakfast_included': 'on'
                                                          })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        group: Group = Group.objects.first()
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'New place')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertGreaterEqual(place.group_id, group.id)
        self.assertTrue(place.latitude, 0)
        user: User = User.objects.first()
        self.assertEqual(user.groups.first(), group)

    def test_create_std_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        fp = SimpleUploadedFile(name='IMG_3745.JPG',
                                content=open('static/places/img/IMG_3745.JPG', 'rb').read(),
                                content_type='image/jpeg')
        response = self.client.post('/places/new/', data={'name': 'New place',
                                                          'picture': fp,
                                                          'category': 'TI',
                                                          'std_price': 12.6,
                                                          'breakfast_included': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        group: Group = Group.objects.first()
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'New place')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertEqual(place.group_id, group.id)
        self.assertGreater(place.latitude, 0)
        user: User = User.objects.first()
        self.assertEqual(user.groups.first(), group)
        room: Room = Room.objects.first()
        self.assertIsInstance(room, Room)
        self.assertEqual(room.place_id, 1)
        self.assertEqual(room.beds, 2)
        self.assertEqual(room.price_per_person, Decimal("12.60"))

    def test_create_bigger_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        fp = SimpleUploadedFile(name='IMG_3745.JPG',
                                content=open('static/places/img/IMG_3745.JPG', 'rb').read(),
                                content_type='image/jpeg')
        response = self.client.post('/places/new/', data={'name': 'New place',
                                                          'picture': fp,
                                                          'category': 'ME',
                                                          'breakfast_included': 'no',
                                                          'std_price': 18.6})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        group: Group = Group.objects.first()
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'New place')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertEqual(place.group_id, group.id)
        self.assertGreater(place.latitude, 0)
        user: User = User.objects.first()
        self.assertEqual(user.groups.first(), group)
        room: Room = Room.objects.last()
        self.assertIsInstance(room, Room)
        self.assertEqual(room.place_id, 1)
        self.assertEqual(room.beds, 6)
        self.assertEqual(room.price_per_person, Decimal("18.60"))
        self.assertEqual(place.valid_rooms().count(), 3)
        place.room_set.add(Room.objects.create(place_id=place.id, price_per_person=0.0, valid_from=date.today()))
        self.assertEqual(place.valid_rooms().count(), 3)
        place.room_set.add(
            Room.objects.create(place_id=place.id, price_per_person=20.0, valid_from=date.today() + timedelta(days=8)))
        self.assertEqual(place.valid_rooms().count(), 3)
        place.room_set.add(Room.objects.create(place_id=place.id, price_per_person=20.0, valid_from=date.today()))
        self.assertEqual(place.valid_rooms().count(), 4)
        self.assertEqual(place.price_high, Decimal('20.0'))
        self.assertEqual(place.price_low, Decimal('18.6'))
        place.room_set.add(
            Room.objects.create(place_id=place.id, price_per_person=20.0, valid_to=date.today() - timedelta(days=8)))
        self.assertEqual(place.valid_rooms().count(), 4)

    def tearDown(self):
        for p in Path("./places/static/img/").glob("IMG_3745_*.jpg"):
            p.unlink()
