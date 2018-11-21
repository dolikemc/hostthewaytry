from django.test.utils import skipIf

from tests.places_tests.base import PlacesPreparedTest


class NewPlaceTest(PlacesPreparedTest):

    @skipIf(True, 'not yet implemented')
    def test_delete_room(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_price(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_soft_delete(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_undelete(self):
        pass
