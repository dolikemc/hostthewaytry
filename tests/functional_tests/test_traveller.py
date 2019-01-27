from django.test.utils import skipIf
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from tests.functional_tests.base import FunctionalTest


class TestWorkflow(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.set_up_traveller()
        self.browser.get(self.live_server_url)
        self.do_logon()

    def test_cannot_change_place(self):
        detail_button = self.get_detail_block('id_place_list')
        detail_button.click()
        with self.assertRaises(NoSuchElementException):
            self.wait_for_find_element_by_id('id_detail_action_update_place')

    def test_login(self):
        self.assertTrue(self.check_if_logged_in())

    def test_start_site(self):
        self.assertTrue(self.check_if_logged_in())
        self.assertTrue(self.browser.find_element_by_id('id_welcome_place_list'))
        self.assertTrue(self.browser.find_element_by_id('id_place_list'))

    def test_icon_bar(self):
        self.assertTrue(self.check_if_logged_in())
        self.assertTrue(self.browser.find_element_by_id('id_navigator_logout'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_search'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_places'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_config'))

    def test_config_menue(self):
        self.assertTrue(self.check_if_logged_in())
        config_menue: WebElement = self.browser.find_element_by_id('id_navigator_config_dropdown')
        config_menue.click()
        self.assertTrue(self.browser.find_element_by_id('id_navigator_profile'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_history'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_filter'))

    @skipIf(True, 'not yet implemented')
    def test_add_comment(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_comment(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_comment(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        self.preview_changes()
        pass

    def test_add_book_request(self):
        detail_button = self.get_detail_block('id_place_list')
        detail_button.click()
        form = self.wait_for_find_element_by_id('id_book_email_form')
        self.assertIsInstance(form, WebElement)
        form.submit()

    @skipIf(True, 'not yet implemented')
    def test_add_logged_book_request(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_logged_book_request(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        pass

    def logon(self):
        pass

    def goto_traveller_area(self):
        pass

    def open_detail(self):
        pass

    def preview_changes(self):
        pass
