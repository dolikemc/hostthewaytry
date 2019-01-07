from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from tests.places_tests.base import PlacesPreparedTest
from traveller.models import PlaceAccount, User


class CreateTest(PlacesPreparedTest):

    def test_register(self):
        self.set_up_staff()
        Group.objects.create(name='Worker')
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post('/traveller/register/', {'password1': pwd, 'password2': pwd, 'email': 'fl@c.com'})
        self.assertRedirects(response, '/traveller/user/2/0/')
        response = self.client.post('/traveller/user/2/0/',
                                    {'screen_name': 'fl', 'unique_name': 'fl', 'email': 'fl@c.com'})
        self.assertRedirects(response, '/admin/')
        user = User.objects.get(id=2)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual('fl', user.display_name)
        self.assertTrue(user.groups.filter(name='Worker').exists())

    def test_add_admin_to_place(self):
        self.set_up_place_admin()
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post(f'/traveller/register/{self.last_place_id}/', {'password1': pwd, 'password2': pwd,
                                                                                   'email': 'fl@c.com'})
        self.assertRedirects(response, f'/traveller/user/2/{self.last_place_id}/')
        response = self.client.post(response.url, {'screen_name': 'a', 'unique_name': 'a', 'email': 'fl@c.com'})
        self.assertRedirects(response, f'/places/update/place/{self.last_place_id}/')
        user = User.objects.get(id=2)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual('a', user.display_name)
        self.assertTrue(user.groups.filter(name__iexact='PlaceAdmin').exists())

    def test_change_myself(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(f'/traveller/user/{self.user.id}/0/',
                                    {'screen_name': 'a', 'unique_name': 'a', 'email': 'fl@c.com'})
        self.assertRedirects(response, '/places/')
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual('a', user.display_name)
        self.assertTrue(user.groups.filter(name__iexact='Traveller').exists())
