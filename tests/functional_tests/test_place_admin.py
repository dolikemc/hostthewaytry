from django.test.utils import skipIf
from selenium.common.exceptions import NoSuchElementException

from tests.functional_tests.base import FunctionalTest
from traveller.models import PlaceAccount


class PlacerAdminTest(FunctionalTest):

    def test_cannot_change_place(self):
        self.browser.get(self.live_server_url)
        self.set_up_traveller()
        self.do_logon()
        detail_button = self.wait_for_find_element_by_id('id_place_card_' + str(self.last_place_id))
        detail_button.click()
        change_button = self.wait_for_find_element_by_id('id_detail_action_update_place')
        change_button.click()
        with self.assertRaises(NoSuchElementException):
            self.wait_for_find_element_by_id('id_who_lives_here')

    def test_can_change_place(self):
        self.set_up_place_admin()
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        self.browser.get(self.live_server_url)
        self.do_logon()
        detail_button = self.wait_for_find_element_by_id('id_place_card_' + str(self.last_place_id))
        detail_button.click()
        change_button = self.wait_for_find_element_by_id('id_detail_action_update_place')
        change_button.click()
        # check just one item in the edit screen
        self.wait_for_find_element_by_id('id_who_lives_here')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_register_traveller(self):
        self.browser.get(self.live_server_url)
        self.set_up_staff()
        self.do_logon()
        register_button = self.wait_for_find_element_by_id('id_navigator_register_worker')
        register_button.click()
        self.assertIn('Create User', self.browser.title)
        username = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        username.send_keys('place@admin.com')
        password1.send_keys('DodoGaga')
        password2.send_keys('DodoGaga')
        submit = self.wait_for_find_element_by_id('id_register_submit')
        submit.click()
        submit2 = self.wait_for_find_element_by_id('id_create_user_submit')
        self.assertIn('HOST THE WAY', self.browser.title)


class TestWorkflow(FunctionalTest):
    @skipIf(True, 'not yet implemented')
    def test_login(self):
        self.logon()
        pass

    @skipIf(True, 'not yet implemented')
    def test_start_site(self):
        self.logon()
        pass

    @skipIf(True, 'not yet implemented')
    def test_place_admin_screen(self):
        self.logon()
        self.goto_admin_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_place(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_address(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_price(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_change_price(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_price(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_room(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_change_room(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_room(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_admin(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_change_admin(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_admin(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_save_changes(self):
        self.logon()
        self.goto_admin_area()
        self.open_detail()
        self.preview_changes()
        pass

    def logon(self):
        pass

    def goto_admin_area(self):
        pass

    def open_detail(self):
        pass

    def preview_changes(self):
        pass
