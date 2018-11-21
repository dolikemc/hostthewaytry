from django.test.utils import skipIf

from places.models import Place, Room, Price
from tests.places_tests.base import PlacesPreparedTest
from traveller.models import Traveller, PlaceAccount


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
        self.assertTrue(self.client.login(**self.credentials))
        traveller: Traveller = Traveller.objects.get(id=self.user.id)
        traveller.user.groups.add(self.place_admin_group)
        PlaceAccount.objects.create(place_id=self.last_place_id, traveller_id=traveller.id)
        response = self.client.post(f'/places/update/place/{self.last_place_id}/', data=self.std_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/places/{self.last_place_id}/')
        place = Place.objects.get(pk=1)
        self.assertEqual(place.name, self.std_data['name'][0])

    def test_update_place_permission(self):
        self.assertTrue(self.client.login(**self.credentials))
        traveller: Traveller = Traveller.objects.get(id=self.user.id)
        traveller.user.groups.add(self.place_admin_group)
        response = self.client.post(f'/places/update/place/{self.last_place_id}/', data=self.std_data)
        self.assertEqual(response.status_code, 403)


@skipIf('True', 'not yet implemented')
class UpdateRoomTest(PlacesPreparedTest):
    pass


@skipIf('True', 'not yet implemented')
class UpdatePriceTest(PlacesPreparedTest):
    pass
