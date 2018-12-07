from pathlib import Path

from django.contrib.auth.models import Group, Permission, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from traveller.models import User


class RoleMixin(object):
    user = None
    group = None

    @property
    def credentials(self):
        return {'email': 'test@user.com', 'password': 'secret'}

    def set_up_anonymous(self):
        self.user = AnonymousUser
        self.group = Group.objects.create(name='Anonymous')

    def set_up_traveller(self):
        self.user = User.objects.create_user(**self.credentials, is_staff=False)
        # todo: permissions (post_comments, add_area_features)
        self.group = Group.objects.create(name='Traveller')
        self.user.groups.add(self.group)
        return self.user

    def set_up_place_admin(self):
        self.user = User.objects.create_user(**self.credentials, is_staff=False)
        self.group: Group = Group.objects.create(name='PlaceAdmin')
        for permission in Permission.objects.filter(codename__in=['delete_place', 'change_place', 'add_user',
                                                                  'change_user', 'view_place']):
            self.group.permissions.add(permission)
        self.user.groups.add(self.group)
        return self.user

    def set_up_worker(self):
        self.user = User.objects.create_user(**self.credentials, is_staff=False)
        self.group: Group = Group.objects.create(name='Worker')
        # todo: permissions (post_comments, add_area_features)
        for permission in Permission.objects.filter(codename__in=['add_place', 'add_user', 'change_user',
                                                                  'delete_user', 'view_place']):
            self.group.permissions.add(permission)
        self.user.groups.add(self.group)
        return self.user

    def set_up_staff(self):
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.group = Group.objects.create(name='Staff')
        for permission in Permission.objects.filter(codename__in=['change_place', 'add_user', 'change_user',
                                                                  'add_place', 'delete_place']):
            self.group.permissions.add(permission)
        self.user.groups.add(self.group)


class BaseTest(TestCase, RoleMixin):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.last_place_id = 0
        self.image_with_exif = 'IMG_3745.JPG'
        self.image_without_exif = 'hosttheway.jpg'
        self.image_path = 'img'

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
