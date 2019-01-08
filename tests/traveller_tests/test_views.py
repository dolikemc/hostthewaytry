from django.http.response import HttpResponse

from tests.base import BaseTest
from traveller.models import User


class ModelTest(BaseTest):
    def test_login(self):
        self.set_up_staff()
        response: HttpResponse = self.client.post('/traveller/login/', self.credentials)
        self.assertRedirects(response, '/admin/places/place/?deleted__exact=0&reviewed__exact=0')

    def test_not_active_user(self):
        self.set_up_staff()
        user = User.objects.get(id=self.user.id)
        user.is_active = False
        user.save()
        response: HttpResponse = self.client.post('/traveller/login/', self.credentials)
        self.assertContains(response, 'User could not be authenticated')
        self.assertNotContains(response, 'This email already exists.')

    def test_clean_password(self):
        self.set_up_staff()
        response: HttpResponse = self.client.post('/traveller/login/', {'email': self.credentials['email'],
                                                                        'password': 'wrong'})
        self.assertContains(response, 'User could not be authenticated')

    def test_change_user(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response: HttpResponse = self.client.get(f'/traveller/user/{self.user.id}/0/')
        self.assertContains(response, 'test@user.com')

    def test_change_staff_user(self):
        self.set_up_staff()
        self.assertTrue(self.client.login(**self.credentials))
        response: HttpResponse = self.client.get(f'/traveller/update/user/{self.user.id}/')
        self.assertContains(response, 'test@user.com')

    def test_change_another_user(self):
        self.set_up_superuser()
        user = User.objects.create(email='another@user.com', unique_name='another', screen_name='another')
        self.assertTrue(self.client.login(**self.credentials))
        response: HttpResponse = self.client.get(f'/traveller/update/user/{user.id}/')
        self.assertContains(response, 'another@user.com')
