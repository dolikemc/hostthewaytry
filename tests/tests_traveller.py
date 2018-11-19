from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from places.models import Place


# Create your tests here.

class TestTravellerMaint(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True)

    def test_register(self):
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post('/places/register/', {'password1': pwd, 'password2': pwd, 'username': 'fl'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/user/0/2/')


class AddUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        # todo: should not need stuff policies, just allowance to add places
        User.objects.create_user(**self.credentials, is_staff=True)
        Group.objects.create(name='Test')
        Place.objects.create(name='Test', group_id=1)

    def test_add_admin_to_place(self):
        self.assertTrue(self.client.login(**self.credentials))
        pwd = make_password('zegwugr643267')
        response = self.client.post('/places/register/1/', {'password1': pwd, 'password2': pwd, 'username': 'fl'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/user/1/2/')
        user = User.objects.filter(groups__in=[1]).first()
        self.assertIsInstance(user, User)
        response = self.client.post('/places/user/1/2/', {'email': 'a@b.de', 'first_name': 'a', 'last_name': 'b'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
