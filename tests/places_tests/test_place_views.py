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
