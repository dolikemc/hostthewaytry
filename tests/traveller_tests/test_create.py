from django.contrib.auth.hashers import make_password

from tests.places_tests.base import PlacesPreparedTest
from traveller.models import PlaceAccount


class CreateTest(PlacesPreparedTest):

    def test_register(self):
        self.set_up_staff()
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post('/traveller/register/', {'password1': pwd, 'password2': pwd, 'email': 'fl@c.com'})
        self.assertRedirects(response, '/traveller/user/2/0/')

    def test_add_admin_to_place(self):
        self.set_up_place_admin()
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post(f'/traveller/register/{self.last_place_id}/', {'password1': pwd, 'password2': pwd,
                                                                                   'email': 'fl@c.com'})
        self.assertRedirects(response, f'/traveller/user/2/{self.last_place_id}/')
        response = self.client.post(response.url, {'unique_name': 'a', 'email': 'fl@c.com'})
        self.assertRedirects(response, f'/places/update/place/{self.last_place_id}/')
