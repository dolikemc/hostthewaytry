from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase, Client

from .image_filed_extend import ImageFieldExtend
from .models import Place


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

    def test_use_template(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/add/')
        self.assertTemplateUsed(response, template_name='places/create_place.html')

    def test_post_minimal_data(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/add/', data={'name': 'test'})
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.url, '/places/1/')

    def test_post_file_load(self):
        self.assertTrue(self.client.login(**self.credentials))
        fp = SimpleUploadedFile(name='places/static/img/IMG_3745.JPG', content=b'file_content', content_type='file/*')
        response = self.client.post('/places/add/', data={'name': 'test file upload', 'picture': fp})
        self.assertEqual(response.status_code, 200)


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
