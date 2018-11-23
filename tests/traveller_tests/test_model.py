from django.contrib.auth.models import AbstractBaseUser

from tests.base import BaseTest
from traveller.models import User


class ModelTest(BaseTest):

    def test_traveller_string(self):
        self.set_up_staff()
        traveller = User.objects.get(id=self.user.id)
        self.assertEqual('a@b.com', str(traveller))

    def test_user_model(self):
        self.set_up_staff()
        user = User.objects.get(id=1)
        self.assertIsInstance(user, AbstractBaseUser)
