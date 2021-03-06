from selenium.common.exceptions import NoSuchElementException

from tests.functional_tests.base import FunctionalTest


class LogonTest(FunctionalTest):

    def test_can_logon(self):
        self.browser.get(self.live_server_url)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_navigator_logout')
        self.set_up_staff()
        self.do_logon()
        self.assertTrue(self.check_if_logged_in())

    def test_can_logout(self):
        self.browser.get(self.live_server_url)
        self.set_up_staff()
        self.do_logon()
        logout_button = self.wait_for_find_element_by_id('id_navigator_logout')
        logout_button.click()
        self.wait_for_find_element_by_id('id_navigator_login', raise_exception=False)
        self.assertFalse(self.check_if_logged_in())

    def test_can_logon_wo_stuff(self):
        self.browser.get(self.live_server_url)
        self.set_up_traveller()
        self.do_logon()
        self.assertTrue(self.check_if_logged_in())
