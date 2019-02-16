from django.http.response import HttpResponse
from django.shortcuts import reverse

from tests.base import BaseTest
from traveller.models import User


class ModelTest(BaseTest):
    def test_login_staff(self):
        self.set_up_staff()
        response: HttpResponse = self.client.post('/traveller/login/', self.credentials)
        self.assertRedirects(response, '/admin/places/place/?deleted__exact=0&reviewed__exact=0')

    def test_login_staff_get(self):
        response: HttpResponse = self.client.get('/traveller/login/')
        self.assertTemplateUsed(response, 'traveller/login.html')

    def test_register_staff_get(self):
        response: HttpResponse = self.client.get('/traveller/register/')
        self.assertTemplateUsed(response, 'traveller/register.html')

    def test_login_place_admin(self):
        self.set_up_place_admin()
        response: HttpResponse = self.client.post('/traveller/login/', self.credentials)
        self.assertRedirects(response, reverse('places:place_admin'))

    def test_login_worker(self):
        self.set_up_worker()
        response: HttpResponse = self.client.post('/traveller/login/', self.credentials)
        self.assertRedirects(response, reverse('places:worker'))

    def test_login_traveller(self):
        self.set_up_traveller()
        response: HttpResponse = self.client.post('/traveller/login/', self.credentials)
        self.assertRedirects(response, reverse('places:index'))

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

    def test_register_with_wrong_password(self):
        self.set_up_staff()
        response: HttpResponse = self.client.post('/traveller/register/', data={'email': 'ab@b.com',
                                                                                'password1': 'zzzrtzt',
                                                                                'password2': 'zzzztzt'})
        self.assertContains(response, 'id_password')
