from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from django.contrib.auth.models import User, Permission, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from places.models import Place, Room, Price
from traveller.models import Traveller, PlaceAccount


class NewPlaceProcess(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
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
        traveller = Traveller.objects.get(id=1)
        self.assertIsInstance(traveller, Traveller)
        place_account: PlaceAccount = PlaceAccount.objects.filter(traveller_id=traveller.id).first()
        self.assertIsInstance(place_account, PlaceAccount)
        self.assertEqual(place_account.place_id, 1)
        place: Place = Place.objects.get(id=1)
        self.assertTrue(place.latitude, 0)
        self.assertIsInstance(traveller, Traveller)
        self.assertEqual('testuser', traveller.user.username)

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
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertGreater(place.latitude, 0)
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
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertGreater(place.latitude, 0)
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
        for p in Path("static/places/img/").glob("IMG_3745_*.jpg"):
            p.unlink()


class EditPlace(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)
        group: Group = Group.objects.create(name='PlaceEditor')
        permission: Permission = Permission.objects.filter(codename='change_place').first()
        group.permissions.add(permission)
        traveller: Traveller = Traveller.objects.get(id=1)
        traveller.user.groups.add(group)
        Place.objects.create(name='TestOne')
        place: Place = Place.objects.get(id=1)
        PlaceAccount.objects.create(place_id=place.id, traveller_id=traveller.id)
        Place.objects.create(name='TestTwo')
        Room.objects.create(place_id=1, room_number='01')
        Room.objects.create(place_id=1, room_number='02')
        Price.objects.create(place_id=1)
        Price.objects.create(place_id=1)
        self.std_data = {'name': ['Das Dreieck'], 'description': ['die Liebste'], 'contact_type': ['PO'],
                         'street': [''], 'city': [''], 'country': [''], 'address_add': [''], 'phone': [''],
                         'mobile': [''], 'website': [''], 'languages': ['EN'], 'who_lives_here': [''],
                         'parking': ['on'], 'wifi': ['on'], 'own_key': ['on'], 'max_stay': ['365'], 'min_stay': ['1'],
                         'category': ['SM'], 'meals': ['BR'], 'meal_example': [''], 'picture': [''], 'longitude': [''],
                         'latitude': [''], 'currency': ['EUR'], 'currencies': ['€'], 'check_out_time': ['12'],
                         'check_in_time': ['14'], 'priority_valid_until': [''], 'priority_category': ['NA']}

    def test_setup(self):
        response = self.client.get('/places/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/places/2/')
        self.assertEqual(response.status_code, 200)
        place = Place.objects.get(pk=1)
        self.assertEqual(place.name, 'TestOne')
        place = Place.objects.get(pk=2)
        self.assertEqual(place.name, 'TestTwo')
        rooms = Room.objects.filter(place_id=1)
        self.assertEqual(rooms.count(), 2)
        price = Price.objects.filter(place_id=1)
        self.assertEqual(price.count(), 2)

    def test_update_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/update/place/1/', data=self.std_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        place = Place.objects.get(pk=1)
        self.assertEqual(place.name, 'Das Dreieck')
