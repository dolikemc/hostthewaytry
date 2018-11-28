from django.contrib.auth.hashers import make_password

from tests.places_tests.base import PlacesPreparedTest


class CreateTest(PlacesPreparedTest):

    def test_register(self):
        self.set_up_staff()
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post('/traveller/register/', {'password1': pwd, 'password2': pwd, 'email': 'fl@c.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/traveller/user/0/2/')

    def test_add_admin_to_place(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post(f'/traveller/register/{self.last_place_id}/', {'password1': pwd, 'password2': pwd,
                                                                                   'email': 'fl@c.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/traveller/user/{self.last_place_id}/2/')
        response = self.client.post(response.url, {'screen_name': 'a'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/{self.last_place_id}/')
