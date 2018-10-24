from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase, Client

from .image_filed_extend import ImageFieldExtend
from .models import Place, Price, Room


class ExifData(TestCase):
    def test_no_location(self):
        file = ImageFieldExtend(
            name='./places/static/img/hosttheway.jpg')

        data = file.get_lat_lon()
        self.assertEqual(data, (None, None))

    def test_file_location(self):
        file = ImageFieldExtend(
            name='./places/static/img/IMG_3745.JPG')

        data = file.get_lat_lon()
        self.assertAlmostEquals(data[0], 48.1367, 4)
        self.assertAlmostEquals(data[1], 11.5763, 4)

    def test_file_location_already_open(self):
        file = ImageFieldExtend(
            name='./places/static/img/IMG_3745.JPG')
        fp = Image.open(file.name)
        data = file.get_lat_lon(fp)
        self.assertAlmostEquals(data[1], 11.5763, 4)
        self.assertAlmostEquals(data[0], 48.1367, 4)


class CreateScreen(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)
        self.std_data = {'name': ['Da'], 'contact_type': ['NA'], 'street': [''], 'city': [''], 'country': ['dE'],
                         'address_add': [''], 'phone': [''], 'mobile': [''], 'description': [''],
                         'languages': ['EN'], 'who_lives_here': [''], 'currency': ['EUR'],
                         'maximum_of_guests': ['1'], 'meals': ['NO'], 'meal_example': [''], 'wifi': ['on'],
                         'max_stay': ['365'], 'min_stay': ['1'], 'currencies': ['€'], 'check_out_time': ['12'],
                         'check_in_time': ['14'], 'category': ['NA'], }

    def test_use_template(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/add/')
        self.assertTemplateUsed(response, template_name='places/create_place.html')

    def test_post_minimal_data(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/add/', data=self.std_data)
        place = Place.objects.first()
        self.assertEqual(place.country, 'DE')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')

    def test_post_file_load(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.std_data['picture'] = SimpleUploadedFile(name='IMG_3745.JPG',
                                                      content=open('places/static/img/IMG_3745.JPG', 'rb').read(),
                                                      content_type='image/jpeg')
        # self.assertIsInstance(self.std_data['picture'], InMemoryUploadedFile)
        self.std_data['name'] = 'test file upload'
        response = self.client.post('/places/add/', data=self.std_data)
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.picture.name[:8], 'IMG_3745')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')


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
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)

    def test_admin(self):
        # Issue a GET request.
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_on_start(self):
        # Issue a GET request.
        response = self.client.get('/places/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_divisons(self):
        # Issue a GET request.
        response: HttpResponse = self.client.get('/places/')
        self.assertContains(response, 'places', status_code=200)
        self.assertInHTML('<title>HOST THE WAY</title>', str(response.content))

    def test_index_template(self):
        response = self.client.get('/places/')
        self.assertTemplateUsed(response, template_name='places/index.html')

    def tearDown(self):
        for p in Path("./places/static/img/").glob("hosttheway_*.jpg"):
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
                                content=open('places/static/img/IMG_3745.JPG', 'rb').read(),
                                content_type='image/jpeg')
        response = self.client.post('/places/new/', data={'name': 'New place', 'picture': fp, 'category': 'NA'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        group: Group = Group.objects.first()
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'New place')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertEqual(place.group_id, group.id)
        self.assertTrue(place.latitude > 0)
        user: User = User.objects.first()
        self.assertEqual(user.groups.first(), group)

    def test_create_std_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        fp = SimpleUploadedFile(name='IMG_3745.JPG',
                                content=open('places/static/img/IMG_3745.JPG', 'rb').read(),
                                content_type='image/jpeg')
        response = self.client.post('/places/new/', data={'name': 'New place',
                                                          'picture': fp,
                                                          'category': 'TI',
                                                          'std_price': 12.6})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        group: Group = Group.objects.first()
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'New place')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertEqual(place.group_id, group.id)
        self.assertTrue(place.latitude > 0)
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
                                content=open('places/static/img/IMG_3745.JPG', 'rb').read(),
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
        self.assertTrue(place.latitude > 0)
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


class EditPlace(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)
        Place.objects.create(name='TestOne')
        Place.objects.create(name='TestTwo')
        Room.objects.create(place_id=1, room_number='01')
        Room.objects.create(place_id=1, room_number='02')
        Price.objects.create(place_id=1)
        Price.objects.create(place_id=1)
        self.std_data = {'form-TOTAL_FORMS': ['1'], 'form-INITIAL_FORMS': ['1'], 'form-MIN_NUM_FORMS': ['0'],
                         'form-MAX_NUM_FORMS': ['1'], 'form-0-name': ['TestCase'], 'form-0-contact_first_name': [''],
                         'form-0-contact_last_name': ['owner'], 'form-0-contact_type': ['NA'], 'form-0-street': [''],
                         'form-0-city': [''], 'form-0-country': [''], 'form-0-address_add': [''], 'form-0-phone': [''],
                         'form-0-mobile': [''], 'form-0-maximum_of_guests': ['1'],
                         'form-0-languages': ['EN'], 'form-0-who_lives_here': [''],
                         'form-0-room_add': [''], 'form-0-currency': ['EUR'], 'form-0-category': ['NA'],
                         'form-0-meals': ['NO'], 'form-0-meal_example': [''], 'form-0-wifi': ['on'],
                         'form-0-description': [''], 'form-0-picture': [''], 'form-0-longitude': ['43.511005555555556'],
                         'form-0-latitude': ['16.444283333333335'], 'form-0-max_stay': ['365'],
                         'form-0-min_stay': ['1'], 'form-0-currencies': ['€'], 'form-0-check_out_time': ['12'],
                         'form-0-check_in_time': ['14'], 'form-0-id': ['1'], 'price-TOTAL_FORMS': ['1'],
                         'price-INITIAL_FORMS': ['0'], 'price-MIN_NUM_FORMS': ['0'], 'price-MAX_NUM_FORMS': ['3'],
                         'price-0-place': ['1'], 'price-0-description': [''], 'price-0-value': ['0.0'],
                         'price-0-currency': ['EUR'], 'price-0-category': ['CL'], 'price-0-id': [''],
                         'room-TOTAL_FORMS': ['1'],
                         'room-INITIAL_FORMS': ['0'], 'room-MIN_NUM_FORMS': ['0'], 'room-MAX_NUM_FORMS': ['1'],
                         'room-0-place': ['1'], 'room-0-room_number': ['01'], 'room-0-beds': ['2'],
                         'room-0-price_per_person': ['0.0'], 'room-0-price_per_room': ['0.0'],
                         'room-0-currency': ['EUR'], 'room-0-valid_from': ['2018-01-01'],
                         'room-0-valid_to': ['2018-12-31'], 'room-0-bathroom': ['on'], 'room-0-room_add': [''],
                         'room-0-pets': ['on'], 'room-0-family': ['on'], 'room-0-id': ['']}

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
        response = self.client.post('/places/update/1/', data=self.std_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        place = Place.objects.get(pk=1)
        self.assertEqual(place.name, 'TestCase')


class AddUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        # todo: should not need stuff policies, just allowance to add places
        User.objects.create_user(**self.credentials, is_staff=True)
        Group.objects.create(name='Test')
        Place.objects.create(name='Test', group_id=1)

    def test_add_admin_to_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/user/1/', data=
        {'email': 'a@b.de', 'password': 'zegwugr643267', 'first_name': 'f', 'last_name': 'l', 'username': 'fl'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        user = User.objects.filter(groups__in=[1]).first()
        self.assertIsInstance(user, User)


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
