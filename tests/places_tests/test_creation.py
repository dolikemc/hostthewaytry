from datetime import date, timedelta
from decimal import Decimal

from places.models import Place, Room, PlaceAccount
from tests.places_tests.base import PlacesTest
from traveller.models import User


class NewPlaceTest(PlacesTest):

    def test_create_minimal_place(self):
        self.set_up_worker()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/new/', data={'name': 'New place', 'picture': self.get_file_pointer(),
                                                          'category': 'NA', 'std_price': '12.20',
                                                          'breakfast_included': 'on'
                                                          })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        traveller = User.objects.get(id=self.user.id)
        self.assertIsInstance(traveller, User)
        place_account: PlaceAccount = PlaceAccount.objects.filter(user_id=traveller.id).first()
        self.assertIsInstance(place_account, PlaceAccount)
        self.assertEqual(place_account.place_id, 1)
        place: Place = Place.objects.get(id=1)
        self.assertTrue(place.latitude, 0)
        self.assertIsInstance(traveller, User)
        self.assertEqual('test@user.com', traveller.email)

    def test_create_std_place(self):
        self.set_up_worker()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/new/', data={'name': 'New place',
                                                          'picture': self.get_file_pointer(),
                                                          'category': 'TI',
                                                          'std_price': 12.6,
                                                          'breakfast_included': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertGreater(place.latitude, 0)
        room: Room = Room.objects.first()
        self.assertIsInstance(room, Room)
        self.assertEqual(room.place_id, 1)
        self.assertEqual(room.beds, 2)
        self.assertEqual(room.price_per_person, Decimal("12.60"))

    # noinspection PyArgumentList
    def test_create_bigger_place(self):
        self.set_up_worker()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/new/', data={'name': 'New place',
                                                          'picture': self.get_file_pointer(),
                                                          'category': 'ME',
                                                          'breakfast_included': 'no',
                                                          'std_price': 18.6})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        place: Place = Place.objects.first()
        self.assertEqual(place.id, 1)
        self.assertGreater(place.latitude, 0)
        room: Room = Room.objects.last()
        self.assertIsInstance(room, Room)
        self.assertEqual(room.place_id, 1)
        self.assertEqual(room.beds, 6)
        self.assertEqual(room.price_per_person, Decimal("18.60"))
        self.assertEqual(place.valid_rooms().count(), 3)
        place.room_set.add(Room.objects.create(place_id=place.id, price_per_person=0.0, valid_from=date.today()))
        self.assertEqual(place.valid_rooms().count(), 3)
        place.room_set.add(
            Room.objects.create(place_id=place.id, price_per_person=20.0, valid_from=date.today() + timedelta(days=8)))
        self.assertEqual(place.valid_rooms().count(), 3)
        place.room_set.add(Room.objects.create(place_id=place.id, price_per_person=20.0, valid_from=date.today()))
        self.assertEqual(place.valid_rooms().count(), 4)
        self.assertEqual(place.price_high, Decimal('20.0'))
        self.assertEqual(place.price_low, Decimal('18.6'))
        place.room_set.add(
            Room.objects.create(place_id=place.id, price_per_person=20.0, valid_to=date.today() - timedelta(days=8)))
        self.assertEqual(place.valid_rooms().count(), 4)

    def test_use_template(self):
        self.set_up_worker()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/places/new/')
        self.assertTemplateUsed(response, template_name='places/create_place_minimal.html')

    def test_post_minimal_data(self):
        self.set_up_worker()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post('/places/new/', data=self.std_data)
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
        self.assertEqual(place.name, 'Da')
        self.assertEqual(place.country, 'DE')

    def test_post_file_load(self):
        self.set_up_worker()
        self.assertTrue(self.client.login(**self.credentials))
        self.std_data['picture'] = self.get_file_pointer()
        # self.assertIsInstance(self.std_data['picture'], InMemoryUploadedFile)
        self.std_data['name'] = 'test file upload'
        response = self.client.post('/places/new/', data=self.std_data)
        place = Place.objects.first()
        self.assertIsInstance(place, Place)
        self.assertEqual(place.picture.name[:8], self.image_with_exif[:8])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/places/1/')
