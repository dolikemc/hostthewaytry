from pathlib import Path

from django.contrib.auth.models import User, Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client


class BaseTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        # Stuff user
        self.credentials = {
            'username': 'test_user',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials, is_staff=True, email='a@b.com')

        group: Group = Group.objects.create(name='PlaceAdmin')
        permission: Permission = Permission.objects.filter(codename='change_place').first()
        group.permissions.add(permission)
        self.place_admin_group = group

        self.last_place_id = 0

        self.image_with_exif = 'IMG_3745.JPG'
        self.image_without_exif = 'hosttheway.jpg'
        self.image_path = 'static/places/img'

    def get_file_pointer(self, with_exif: bool = True):
        if with_exif:
            return SimpleUploadedFile(name=self.image_with_exif,
                                      content=open('/'.join([self.image_path, self.image_with_exif]), 'rb').read(),
                                      content_type='image/jpeg')
        return SimpleUploadedFile(name=self.image_without_exif,
                                  content=open('/'.join([self.image_path, self.image_without_exif]), 'rb').read(),
                                  content_type='image/jpeg')

    def tearDown(self):
        # remove the created image files
        for p in Path(self.image_path).glob("IMG_3745_*.jpg"):
            p.unlink()
        for p in Path(self.image_path).glob("hosttheway_*.jpg"):
            p.unlink()
