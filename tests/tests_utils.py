from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from places.models import Place
from utils.file import ImageX


class ExifData(TestCase):
    def test_no_location(self):
        file = ImageX(name='./places/static/img/hosttheway.jpg')
        self.assertTrue(file.open())
        self.assertEqual(file.longitude, 0.00)

    def test_file_location(self):
        file = ImageX(name='./places/static/img/IMG_3745.JPG')
        self.assertTrue(file.open())
        self.assertAlmostEquals(file.latitude, 48.1367, 4)
        self.assertAlmostEquals(file.longitude, 11.5763, 4)

    def test_orientation_wrong(self):
        file = ImageX(name='./places/static/img/IMG_3745.JPG')
        self.assertTrue(file.open())
        self.assertEqual(6, file.orientation)
        file.correct_orientation()
        self.assertEqual(1, file.orientation)
        file.resize()
        self.assertEqual(1, file.orientation)

    def test_orientation(self):
        file = ImageX(name='./places/static/img/orig.jpg')
        self.assertTrue(file.open())
        self.assertEqual(0, file.orientation)

    def test_save_method(self):
        Place.objects.create(name='Test')
        place = Place.objects.get(id=1)
        place.picture = SimpleUploadedFile(name='IMG_3745.JPG',
                                           content=open('places/static/img/IMG_3745.JPG', 'rb').read(),
                                           content_type='image/jpeg')
        place.picture.name = 'IMG_3745_X.JPG'
        place.save()
        place = Place.objects.get(id=1)
        self.assertIsInstance(place, Place)
        self.assertGreater(place.latitude, 0)
        # print(place.latitude)

    def tearDown(self):
        for p in Path("./places/static/img/").glob("IMG_3745_*.JPG"):
            p.unlink()
