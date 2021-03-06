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

    def test_config_menu(self):
        self.assertTrue(self.check_if_logged_in())
        config_menu: WebElement = self.browser.find_element_by_id('id_navigator_config_dropdown')
        self.assertIsInstance(config_menu, WebElement)
        config_menu.click()
        self.assertTrue(self.browser.find_element_by_id('id_navigator_profile'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_history'))
        self.assertTrue(self.browser.find_element_by_id('id_navigator_filter'))

    def test_see_history(self):
        self.assertTrue(self.check_if_logged_in())
        config_menu: WebElement = self.browser.find_element_by_id('id_navigator_config_dropdown')
        self.assertIsInstance(config_menu, WebElement)
        config_menu.click()
        history: WebElement = self.browser.find_element_by_id('id_navigator_history')
        self.assertIsInstance(history, WebElement)
        history.click()
        self.assertTrue(self.wait_for_find_element_by_id('id_place_list_maintenance', raise_exception=False))
        # todo: other histories, articles and bookings

    def test_filter(self):
        self.assertTrue(self.check_if_logged_in())
        config_menu: WebElement = self.browser.find_element_by_id('id_navigator_config_dropdown')
        self.assertIsInstance(config_menu, WebElement)
        config_menu.click()
        history: WebElement = self.browser.find_element_by_id('id_navigator_filter')
        self.assertIsInstance(history, WebElement)
        history.click()
        self.assertTrue(self.wait_for_find_element_by_id('id_place_list', raise_exception=False))

    @skipIf(True, 'not yet implemented')
    def test_add_comment(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_comment(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_comment(self):
        pass

    def test_add_book_request(self):
        self.assertTrue(self.check_if_logged_in())
        self.browser.get(self.live_server_url + '/places')
        card = self.get_detail_block('id_place_list')
        card.click()
        self.wait_for_find_element_by_id('id_place_detail_bar')
        book = self.browser.find_element_by_id('id_book_place')
        self.assertIsInstance(book, WebElement)
        book.click()
        self.wait_for_find_element_by_id('id_book_email_form', raise_exception=False)
        self.assertTrue(self.browser.find_element_by_id('id_submit_booking'))

    @skipIf(True, 'not yet implemented')
    def test_delete_logged_book_request(self):
        pass
