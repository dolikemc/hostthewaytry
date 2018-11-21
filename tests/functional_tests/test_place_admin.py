from django.contrib.auth.models import Permission, Group
from selenium.common.exceptions import NoSuchElementException

from tests.functional_tests.base import FunctionalTest
from traveller.models import PlaceAccount


class PlacerAdminTest(FunctionalTest):

    def test_cannot_change_place(self):
        self.browser.get(self.live_server_url)
        self.do_logon()
        detail_button = self.wait_for_find_element_by_id('place-card-' + str(self.last_place_id))
        detail_button.click()
        change_button = self.wait_for_find_element_by_id('detail-action-update-place')
        change_button.click()
        with self.assertRaises(NoSuchElementException):
            self.wait_for_find_element_by_id('id_who_lives_here')

    def test_can_change_place(self):
        PlaceAccount.objects.create(place_id=self.last_place_id, traveller_id=self.user.id)
        permission: Permission = Permission.objects.filter(codename='change_place').first()
        permission_user = Permission.objects.filter(codename__endswith='_user')
        group: Group = Group.objects.create(name='PlaceAdmin')
        group.permissions.add(permission)
        # for perm in permission_user:
        #    group.permissions.add(perm)
        self.user.groups.add(group)
        self.browser.get(self.live_server_url)
        self.do_logon()
        detail_button = self.wait_for_find_element_by_id('place-card-' + str(self.last_place_id))
        detail_button.click()
        change_button = self.wait_for_find_element_by_id('detail-action-update-place')
        change_button.click()
        # check just one item in the edit screen
        self.wait_for_find_element_by_id('id_who_lives_here')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_register_traveller(self):
        self.browser.get(self.live_server_url)
        self.do_logon()
        register_button = self.wait_for_find_element_by_id('navigator-register-worker')
        register_button.click()
        self.assertIn('Create User', self.browser.title)
        username = self.browser.find_element_by_id('id_username')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        username.send_keys('place-admin')
        password1.send_keys('DodoGaga')
        password2.send_keys('DodoGaga')
        submit = self.wait_for_find_element_by_id('register-submit')
        submit.click()
        submit2 = self.wait_for_find_element_by_id('create-user-submit')
        self.assertIn('HOST THE WAY', self.browser.title)
