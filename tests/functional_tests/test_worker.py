from django.test.utils import skipIf
from selenium.webdriver.remote.webelement import WebElement

from tests.functional_tests.base import FunctionalTest


class TestWorkflow(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.set_up_worker()
        self.browser.get(self.live_server_url)
        self.do_logon()

    def test_login(self):
        self.assertTrue(self.check_if_logged_in())

    def test_start_site(self):
        self.assertTrue(self.wait_for_find_element_by_id('id_welcome_worker'))

    def test_worker_screen(self):
        self.goto_worker_area()
        self.assertTrue(self.wait_for_find_element_by_id('id_welcome_worker'))
        self.assertTrue(self.wait_for_find_element_by_id('id_create_place'))

    def test_create_place(self):
        self.goto_worker_area()
        button = self.wait_for_find_element_by_id('id_create_place')
        self.assertIsInstance(button, WebElement)
        button.click()
        self.assertTrue(self.wait_for_find_element_by_id('id_create_place_minimal_form'))
        for item in ['id_name', 'id_std_price']:
            self.assertTrue(self.wait_for_find_element_by_id(item))
            field: WebElement = self.browser.find_element_by_id(item)
            field.send_keys('1234')
        button = self.browser.find_element_by_id('id_submit_create_place')
        self.assertIsInstance(button, WebElement)
        button.click()
        self.assertTrue(self.wait_for_find_element_by_id('id_place_detail_name'))

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
    def test_create_admin(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_admin(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_comment(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_comment(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_comment(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_area_highlite(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_area_highlite(self):
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_area_highlite(self):
        self.goto_worker_area()
        pass

    def goto_worker_area(self):
        pass
