from django.test.utils import skipIf

from tests.places_tests.base import PlacesPreparedTest


class NewPlaceTest(PlacesPreparedTest):

    @skipIf(True, 'not yet implemented')
    def test_publish(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_unpublish(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_soft_delete(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_undelete(self):
        pass
