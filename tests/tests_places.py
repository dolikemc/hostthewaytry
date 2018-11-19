from decimal import Decimal
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase, Client

from places.models import Place, Price, Room


class CreateScreen(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True, email='a@b.com')
        self.std_data = {'name': ['Da'], 'contact_type': ['NA'], 'street': [''], 'city': [''], 'country': ['dE'],
                         'address_add': [''], 'phone': [''], 'mobile': [''], 'description': [''],
                         'languages': ['EN'], 'who_lives_here': [''], 'currency': ['EUR'], 'std_price': ['12.20'],
                         'maximum_of_guests': ['1'], 'meals': ['NO'], 'meal_example': [''], 'wifi': ['on'],
                         'max_stay': ['365'], 'min_stay': ['1'], 'currencies': ['€'], 'check_out_time': ['12'],
                         'check_in_time': ['14'], 'category': ['NA'], 'breakfast_included': ['on']}

    def test_use_template(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/new/')
        self.assertTemplateUsed(response, template_name='places/create_place_minimal.html')

    def test_post_minimal_data(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/new/', data=self.std_data)
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        self.assertEqual(place.name, 'Da')
        self.assertEqual(place.country, 'DE')

    def test_post_file_load(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.std_data['picture'] = SimpleUploadedFile(name='IMG_3745.JPG',
                                                      content=open('static/places/img/IMG_3745.JPG', 'rb').read(),
                                                      content_type='image/jpeg')
        # self.assertIsInstance(self.std_data['picture'], InMemoryUploadedFile)
        self.std_data['name'] = 'test file upload'
        response = self.client.post('/places/new/', data=self.std_data)
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.picture.name[:8], 'IMG_3745')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')

    def tearDown(self):
        for p in Path("static/places/img").glob("IMG_3745_*.jpg"):
            p.unlink()


class ListScreen(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        place = Place
        place.objects.create(name='Test')
        place.objects.create(name='Test1')
        place.objects.create(name='Test2')
        place.objects.create(name='Test3')
        place.objects.create(name='TestIt')

    def test_on_start(self):
        # Issue a GET request.
        response = self.client.get('/places/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_divisons(self):
        # Issue a GET request.
        response: HttpResponse = self.client.get('/places/')
        self.assertContains(response, 'places', status_code=200)
        print(str(response.content))
        self.assertInHTML('<title>HOST THE WAY</title>', response.content.decode())

    def test_index_template(self):
        response = self.client.get('/places/')
        self.assertTemplateUsed(response, template_name='places/index.html')

    def tearDown(self):
        for p in Path("./places/static/img").glob("hosttheway_*.jpg"):
            p.unlink()


class RoomScreen(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)
        self.std_data = {'room_number': ['01'], 'beds': ['4'], 'currency': ['EUR'], 'price_per_person': ['20.0'],
                         'price_per_room': ['70.0'], 'valid_from': ['2018-01-01'], 'valid_to': ['2018-12-31'], }
        Place.objects.create(name='TestIt')

    def test_form(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/room/1/')
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        response = self.client.get('/places/room/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/places/room/1/")

    def test_use_template(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/room/1/')
        self.assertTemplateUsed(response, template_name='places/create_detail.html')

    def test_new_room(self):
        self.assertTrue(self.client.login(**self.credentials))
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.id, 1)
        response = self.client.post('/places/room/1/', data=self.std_data)
        room = Room.objects.first()
        self.assertIsInstance(room, Room)
        self.assertEqual(room.place_id, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')


class PriceScreen(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)
        self.std_data = {'description': ['sweet home'], 'value': ['0.0'], 'currency': ['EUR'], 'category': ['CL'],
                         'valid_from': ['2018-01-01'], 'valid_to': ['2018-12-31']}
        Place.objects.create(name='TestIt')

    def test_form(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/price/1/')
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        response = self.client.get('/places/price/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/places/price/1/")

    def test_use_template(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/price/1/')
        self.assertTemplateUsed(response, template_name='places/create_detail.html')

    def test_new_price(self):
        self.assertTrue(self.client.login(**self.credentials))
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.id, 1)
        response = self.client.post('/places/price/1/', data=self.std_data)
        price = Price.objects.first()
        self.assertIsInstance(price, Price)
        self.assertEqual(price.place_id, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')


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
