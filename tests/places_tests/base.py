from places.models import Place, Room, Price
from tests.base import BaseTest


class PlacesTest(BaseTest):
    def setUp(self):
        super().setUp()
        # data dictionary
        self.std_data = {'name': ['Da'], 'contact_type': ['NA'], 'street': [''], 'city': [''], 'country': ['dE'],
                         'address_add': [''], 'phone': [''], 'mobile': [''],
                         'languages': ['EN'], 'who_lives_here': [''], 'std_price': ['12.20'],
                         'maximum_of_guests': ['1'], 'meals': ['NO'], 'meal_example': [''], 'wifi': ['on'],
                         'max_stay': ['365'], 'min_stay': ['1'], 'currencies': ['€'], 'check_out_time': ['12'],
                         'check_in_time': ['14'], 'breakfast_included': ['on'],
                         'room_number': ['01'], 'beds': ['4'], 'price_per_person': ['20.0'],
                         'price_per_room': ['70.0'], 'valid_from': ['2018-01-01'], 'valid_to': ['2018-12-31'],
                         'description': ['sweet home'], 'value': ['0.0'], 'currency': ['EUR'], 'category': ['NA'],
                         }


class PlacesPreparedTest(PlacesTest):
    def setUp(self):
        super().setUp()
        # a couple of places
        place = Place.objects.create(name='TestIt')
        self.last_place_id = place.id
        Room.objects.create(place_id=self.last_place_id, room_number='01')
        self.last_room_id = Room.objects.create(place_id=self.last_place_id, room_number='02').id
        Price.objects.create(place_id=self.last_place_id)
        self.last_price_id = Price.objects.create(place_id=self.last_place_id).id
        place2 = Place.objects.create(name='Da')
        Room.objects.create(place_id=place2.id, room_number='03')
        Price.objects.create(place_id=place2.id)
