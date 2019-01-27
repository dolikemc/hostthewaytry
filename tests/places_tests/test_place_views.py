from django.http import HttpResponse

from tests.places_tests.base import PlacesPreparedTest


class SimpleViewPlaceTest(PlacesPreparedTest):

    def test_on_start(self):
        self.set_up_anonymous()
        # Issue a GET request.
        response = self.client.get('/places/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_division(self):
        self.set_up_anonymous()
        # Issue a GET request.
        response: HttpResponse = self.client.get('/places/')
        self.assertContains(response, 'places', status_code=200)
        self.assertInHTML('<title>HOST THE WAY</title>', response.content.decode())

    def test_index_template(self):
        self.set_up_anonymous()
        response = self.client.get('/places/')
        self.assertTemplateUsed(response, template_name='places/index.html')

    def test_history(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/history/')
        self.assertTemplateUsed(response, template_name='places/histories_index.html')

    def test_worker(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/worker/')
        self.assertTemplateUsed(response, template_name='places/worker_index.html')

    def test_place_admin(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/place_admin/')
        self.assertTemplateUsed(response, template_name='places/place_admin_index.html')

    def test_filter(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/filter/')
        self.assertTemplateUsed(response, template_name='places/filter_index.html')

    def test_profile(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(f'/traveller/user/{self.user.id}/0/')
        self.assertTemplateUsed(response, template_name='traveller/create_place_admin.html')
