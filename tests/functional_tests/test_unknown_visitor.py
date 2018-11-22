from places.models import Place
from tests.functional_tests.base import FunctionalTest


class VisitorTest(FunctionalTest):

    def test_set_up(self):
        self.set_up_anonymous()
        self.assertEqual(4, Place.objects.all().count())

    def test_can_index_places(self):
        self.set_up_anonymous()
        self.browser.get(self.live_server_url + '/places')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_index(self):
        self.set_up_anonymous()
        self.browser.get(self.live_server_url)
        self.assertIn('HOST THE WAY', self.browser.title)
