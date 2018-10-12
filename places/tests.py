from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase, Client

from .image_filed_extend import ImageFieldExtend
from .models import Place, Price


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
        self.std_data = {'name': ['Da'], 'contact_first_name': [''], 'contact_last_name': ['owner'],
                         'contact_type': ['NA'], 'street': [''], 'city': [''], 'country': ['dE'], 'address_add': [''],
                         'phone': [''], 'mobile': [''], 'email': ['hosttheway@gmail.com'], 'email_alt': [''],
                         'languages': ['EN'], 'who_lives_here': [''], 'rooms': ['1'], 'beds': ['2'],
                         'maximum_of_guests': ['1'], 'bathrooms': ['1'], 'room_add': [''], 'pets': ['on'],
                         'family': ['on'], 'meals': ['NO'], 'meal_example': [''], 'wifi': ['on'], 'description': [''],
                         'max_stay': ['365'], 'min_stay': ['1'], 'currencies': ['€'], 'check_out_time': ['12'],
                         'check_in_time': ['14']}

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
