from django.contrib.auth.models import AbstractBaseUser

from tests.base import BaseTest
from traveller.models import User


class ModelTest(BaseTest):

    def test_traveller_string(self):
        self.set_up_staff()
        traveller = User.objects.get(id=self.user.id)
        self.assertEqual('test@user.com', str(traveller))

    def test_user_model(self):
        self.set_up_staff()
        user = User.objects.get(id=1)
        self.assertIsInstance(user, AbstractBaseUser)

    def test_unique_name_from_email(self):
        self.user = User.objects.create(email='next@a.com')
        self.user.create_screen_names()
        self.assertEqual(self.user.email, self.user.display_name)

    def test_unique_name_from_screen_name(self):
        self.set_up_staff()
        self.user.screen_name = 'a'
        self.user.create_screen_names()
        self.assertEqual('a', self.user.display_name)

    def test_unique_name_generated(self):
        User.objects.create(email='next@a.com', screen_name='a', unique_name='a')
        self.set_up_staff()
        self.user.save()
        self.assertEqual(self.user.id, 2)
        self.user.screen_name = 'a'
        self.user.create_screen_names()
        self.assertEqual('a (a2)', self.user.display_name)

    def test_unique_name_from_email_html(self):
        self.user = User.objects.create(email='next@a.com')
        self.user.create_screen_names()
        self.assertIn('<div class="screen-user-name-display">next AT a.com<div>', self.user.display_name_html)

    def test_unique_name_from_screen_name_html(self):
        self.set_up_staff()
        self.user.screen_name = 'a'
        self.user.create_screen_names()
        self.assertIn('a', self.user.display_name)

    def test_unique_name_generated_html(self):
        User.objects.create(email='next@a.com', screen_name='a', unique_name='a')
        self.set_up_staff()
        self.user.save()
        self.assertEqual(self.user.id, 2)
        self.user.screen_name = 'a'
        self.user.create_screen_names()
        self.assertIn('a', self.user.display_name_html)
        self.assertIn('(a2)', self.user.display_name_html)
