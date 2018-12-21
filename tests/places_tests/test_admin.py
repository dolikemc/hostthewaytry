from tests.places_tests.base import PlacesPreparedTest


class NewPlaceTest(PlacesPreparedTest):

    def setUp(self):
        super().setUp()
        self.set_up_staff()

    def test_publish(self):
        self.assertTrue(self.client.login(**self.credentials))
        data = {'action': 'publish', '_selected_action': [self.last_place_id]}
        response = self.client.post('/admin/places/place/?', data)
        self.assertRedirects(response, '/admin/places/place/')

    def test_unpublish(self):
        self.assertTrue(self.client.login(**self.credentials))
        data = {'action': 'unpublish', '_selected_action': [self.last_place_id]}
        response = self.client.post('/admin/places/place/?', data)
        self.assertRedirects(response, '/admin/places/place/')

    def test_soft_delete(self):
        self.assertTrue(self.client.login(**self.credentials))
        data = {'action': 'mark_deleted', '_selected_action': [self.last_place_id]}
        response = self.client.post('/admin/places/place/?', data)
        self.assertRedirects(response, '/admin/places/place/')

    def test_undelete(self):
        self.assertTrue(self.client.login(**self.credentials))
        data = {'action': 'unmark_deleted', '_selected_action': [self.last_place_id]}
        response = self.client.post('/admin/places/place/?', data)
        self.assertRedirects(response, '/admin/places/place/')
