from django.test.utils import skipIf

from places.models import Room, Place, Price
from tests.places_tests.base import PlacesPreparedTest
from traveller.models import PlaceAccount


class NewPlaceTest(PlacesPreparedTest):
    def setUp(self):
        super().setUp()
        self.set_up_place_admin()
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        self.assertTrue(self.client.login(**self.credentials))

    def test_delete_room(self):
        response = self.client.post(f'/places/delete/room/{self.last_room_id}/')
        self.assertRedirects(response, f'/places/update/place/{self.last_place_id}/')
        self.assertFalse(Room.objects.filter(id=self.last_room_id).exists())

    def test_delete_price(self):
        response = self.client.post(f'/places/delete/price/{self.last_price_id}/')
        self.assertRedirects(response, f'/places/update/place/{self.last_place_id}/')
        self.assertFalse(Price.objects.filter(id=self.last_price_id).exists())

    @skipIf(True, 'Not yet implemented')
    def test_soft_delete(self):
        response = self.client.post(f'/places/delete/place/{self.last_place_id}/')
        self.assertRedirects(response, f'/places/')
        self.assertEqual(Place.objects.filter(id=self.last_place_id, deleted=False), None)

    def test_undelete(self):
        response = self.client.post(f'/places/undelete/place/{self.last_place_id}/')
        self.assertRedirects(response, f'/places/update/place/{self.last_place_id}/')
        self.assertEqual(Place.objects.filter(id=self.last_place_id, deleted=False).count(), 1)
