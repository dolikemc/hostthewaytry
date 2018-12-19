from django.test.utils import skipIf

from tests.base import BaseTest
from traveller.forms import ChangeUser, UserCreationForm
from traveller.views import login_user


class ModelTest(BaseTest):
    @skipIf(True, 'not yet implemented')
    def test_not_active_user(self):
        response = self.client.get('/traveller/login/')
        login_user(response)
        pass

    @skipIf(True, 'not yet implemented')
    def test_clean_password(self):
        form = UserCreationForm()
        pass

    @skipIf(True, 'not yet implemented')
    def test_change_user(self):
        form = ChangeUser()
        pass
