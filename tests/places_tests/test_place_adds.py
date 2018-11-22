from places.models import Place, Room, Price
from tests.places_tests.base import PlacesPreparedTest


class RoomScreen(PlacesPreparedTest):

    def test_form(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/room/1/')
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        self.set_up_place_admin()
        response = self.client.get('/places/room/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/places/room/1/")

    def test_use_template(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/room/1/')
        self.assertTemplateUsed(response, template_name='places/create_detail.html')

    def test_new_room(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.id, 1)
        response = self.client.post('/places/room/1/', data=self.std_data)
        room = Room.objects.first()
        self.assertIsInstance(room, Room)
        self.assertEqual(room.place_id, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')


class PriceScreen(PlacesPreparedTest):

    def test_form(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/price/1/')
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        self.set_up_place_admin()
        response = self.client.get('/places/price/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/places/price/1/")

    def test_use_template(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/price/1/')
        self.assertTemplateUsed(response, template_name='places/create_detail.html')

    def test_new_price(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.id, 1)
        # can't use category from place
        self.std_data['category'] = ['CL']
        response = self.client.post('/places/price/1/', data=self.std_data)
        price = Price.objects.first()
        self.assertIsInstance(price, Price)
        self.assertEqual(price.place_id, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
