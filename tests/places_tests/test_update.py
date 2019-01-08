from decimal import Decimal

from places.models import Place, Room, Price
from tests.places_tests.base import PlacesPreparedTest
from traveller.models import PlaceAccount


class UpdatePlaceTest(PlacesPreparedTest):

    def test_setup(self):
        response = self.client.get('/places/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/places/2/')
        self.assertEqual(response.status_code, 200)
        place = Place.objects.get(pk=1)
        self.assertEqual(place.name, 'TestIt')
        place = Place.objects.get(pk=2)
        self.assertEqual(place.name, 'Da')
        rooms = Room.objects.filter(place_id=2)
        self.assertEqual(rooms.count(), 1)
        price = Price.objects.filter(place_id=2)
        self.assertEqual(price.count(), 1)

    def test_update_place(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        response = self.client.post(f'/places/update/place/{self.last_place_id}/', data=self.std_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/{self.last_place_id}/')
        place = Place.objects.get(pk=self.last_place_id)
        self.assertEqual(place.name, self.std_data['name'][0])

    def test_update_place_not_allowed(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(f'/places/update/place/{self.last_place_id}/', data=self.std_data)
        self.assertEqual(response.status_code, 403)
        # self.assertRedirects(response, f'/traveller/login/?next=/places/update/place/{self.last_place_id}/')

    def test_update_address_clean(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        special_data = self.std_data
        special_data['country'] = ['iR']
        response = self.client.post(f'/places/update/place/address/{self.last_place_id}/', data=special_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/{self.last_place_id}/')
        place = Place.objects.get(pk=self.last_place_id)
        self.assertEqual('IR', place.country)

    def test_update_room_clean(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        special_data = self.std_data
        special_data['room_number'] = ['iR']
        response = self.client.post(f'/places/update/room/{self.last_room_id}/', data=special_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/update/place/{self.last_place_id}/')
        room = Room.objects.get(pk=self.last_room_id)
        self.assertEqual('iR', room.room_number)

    def test_update_price_clean(self):
        self.set_up_place_admin()
        self.assertTrue(self.client.login(**self.credentials))
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        special_data = self.std_data
        special_data['value'] = ['99.7']
        special_data['category'] = ['CL']
        response = self.client.post(f'/places/update/price/{self.last_price_id}/', data=special_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/update/place/{self.last_place_id}/')
        price = Price.objects.get(pk=self.last_price_id)
        self.assertAlmostEqual(Decimal(99.7), price.value, 2)
