from django.contrib.auth.hashers import make_password

from tests.places_tests.base import PlacesPreparedTest


class CreateTest(PlacesPreparedTest):

    def test_register(self):
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post('/places/register/', {'password1': pwd, 'password2': pwd, 'username': 'fl'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/user/0/2/')

    def test_add_admin_to_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post(f'/places/register/{self.last_place_id}/', {'password1': pwd, 'password2': pwd,
                                                                                'username': 'fl'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/user/{self.last_place_id}/2/')
        response = self.client.post(response.url, {'email': 'a@b.de', 'first_name': 'a',
                                                   'last_name': 'b'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/{self.last_place_id}/')
