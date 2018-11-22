from selenium.common.exceptions import NoSuchElementException

from tests.functional_tests.base import FunctionalTest


class LogonTest(FunctionalTest):

    def test_can_logon(self):
        self.browser.get(self.live_server_url)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('navigator-logout')
        self.set_up_staff()
        self.do_logon()
        self.assertTrue(self.wait_for_find_element_by_id('navigator-logout'))
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_logout(self):
        self.browser.get(self.live_server_url)
        self.set_up_staff()
        self.do_logon()
        logout_button = self.wait_for_find_element_by_id('navigator-logout')
        logout_button.click()
        with self.assertRaises(NoSuchElementException):
            self.wait_for_find_element_by_id('navigator-logout')

    def test_can_logon_wo_stuff(self):
        self.browser.get(self.live_server_url)
        self.set_up_traveller()
        self.do_logon()
        self.assertTrue(self.wait_for_find_element_by_id('navigator-logout'))
        self.assertIn('HOST THE WAY', self.browser.title)
