from django.contrib.auth.models import AbstractBaseUser
from django.test.utils import skipIf

from tests.base import BaseTest
from traveller.models import User, PlaceAccount


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

    def test_is_worker(self):
        self.set_up_worker()
        self.assertTrue(self.user.is_worker)

    def test_is_traveller(self):
        self.set_up_traveller()
        self.assertTrue(self.user.is_traveller)

    def test_is_place_admin(self):
        self.set_up_place_admin()
        self.assertTrue(self.user.is_place_admin)

    def test_is_anonymous(self):
        self.set_up_anonymous()
        self.assertTrue(self.user.is_anonymous)

    def test_full_name(self):
        self.set_up_staff()
        traveller = User.objects.get(id=self.user.id)
        self.assertEqual('', traveller.get_full_name())

    def test_short_name(self):
        self.set_up_staff()
        traveller = User.objects.get(id=self.user.id)
        self.assertEqual('test@user.com(None)', traveller.get_short_name())

    def test_screen_name(self):
        user = User.objects.create(email='next@a.com', screen_name='a', unique_name='a')
        self.assertEqual('a', user.get_short_name())

    def test_create_superuser(self):
        su = User.objects.create_superuser(email='a@b.com', password='aaaa')
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)

    def test_create_user(self):
        su = User.objects.create_user(email='a@b.com', password='aaaa')
        self.assertFalse(su.is_staff)
        self.assertFalse(su.is_superuser)

    def test_create_no_user_wo_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='aaaa')

    @skipIf(True, 'not yet implemented')
    def test_email_user(self):
        pass

    def test_create_screen_names_unique_name_exists(self):
        user = User.objects.create(email='next@a.com', screen_name='a', unique_name='a')
        user.create_screen_names()
        self.assertEqual('a', user.get_short_name())

    def test_display_name_html(self):
        user = User.objects.create(email='next@a.com', screen_name='a', unique_name='a')
        self.assertEqual('<div class="screen-user-name-display">a<div>', user.display_name_html)

    def test_edit_place_permission_for_superuser(self):
        self.set_up_staff()
        self.assertTrue(PlaceAccount.edit_place_permission(self.user, self.last_place_id))

    def test_edit_place_permission_for_staff(self):
        user = User.objects.create(email='next@a.com', is_staff=True, is_superuser=False)
        self.assertTrue(PlaceAccount.edit_place_permission(user, self.last_place_id))

    def test_edit_place_permission_for_anonymous(self):
        self.set_up_anonymous()
        self.assertFalse(PlaceAccount.edit_place_permission(self.user, self.last_place_id))

    def test_edit_place_permission_for_traveller(self):
        self.set_up_traveller()
        self.assertFalse(PlaceAccount.edit_place_permission(self.user, self.last_place_id))

    def test_edit_place_permission_for_place_admin(self):
        self.set_up_place_admin()
        PlaceAccount.objects.create(user_id=self.user.id, place_id=self.last_place_id)
        self.assertTrue(PlaceAccount.edit_place_permission(self.user, self.last_place_id))

    def test_edit_place_permission_for_other_place_admin(self):
        self.set_up_place_admin()
        self.assertFalse(PlaceAccount.edit_place_permission(self.user, self.last_place_id))
