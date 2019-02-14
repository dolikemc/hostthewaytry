from places.models import Place
from tests.base import BaseTest
from utils.file import ImageX


class ExifData(BaseTest):
    def test_no_location(self):
        file = ImageX(name='/'.join([self.image_path, self.image_without_exif]))
        self.assertTrue(file.open())
        self.assertEqual(file.longitude, 0.00)

    def test_file_location(self):
        file = ImageX(name='/'.join([self.image_path, self.image_with_exif]))
        self.assertTrue(file.open())
        self.assertAlmostEquals(file.latitude, 48.1367, 4)
        self.assertAlmostEquals(file.longitude, 11.5763, 4)

    def test_orientation_wrong(self):
        file = ImageX(name='/'.join([self.image_path, self.image_with_exif]))
        self.assertTrue(file.open())
        self.assertEqual(6, file.orientation)
        file.correct_orientation()
        self.assertEqual(1, file.orientation)
        file.resize()
        self.assertEqual(1, file.orientation)

    def test_orientation(self):
        file = ImageX(name='/'.join([self.image_path, 'orig.jpg']))
        self.assertTrue(file.open())
        self.assertEqual(0, file.orientation)

    def test_save_method(self):
        Place.objects.create(name='Test', created_by=self.user)
        place = Place.objects.get(id=1)
        place.picture = self.get_file_pointer()
        place.picture.name = 'IMG_3745_X.JPG'
        place.clean()
        place.save()
        place = Place.objects.get(id=1)
        self.assertIsInstance(place, Place)
        self.assertGreater(place.latitude, 0)
        # print(place.latitude)
