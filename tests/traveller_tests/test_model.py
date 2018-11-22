from tests.base import BaseTest
from traveller.models import Traveller


class ModelTest(BaseTest):

    def test_traveller_string(self):
        self.set_up_staff()
        traveller = Traveller.objects.get(id=self.user.id)
        self.assertEqual('a@b.com test_user', str(traveller))
