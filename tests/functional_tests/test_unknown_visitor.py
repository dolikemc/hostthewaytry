from django.contrib.auth.models import User

from places.models import Place
from tests.functional_tests.base import FunctionalTest


class VisitorTest(FunctionalTest):

    def test_set_up(self):
        self.assertEqual(4, Place.objects.all().count())
        self.assertEqual(1, User.objects.filter(is_staff=True).count())

    def test_can_index_places(self):
        self.browser.get(self.live_server_url + '/places')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_index(self):
        self.browser.get(self.live_server_url)
        self.assertIn('HOST THE WAY', self.browser.title)
