import logging

from django.test.utils import skipIf
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from tests.functional_tests.base import FunctionalTest
from traveller.models import PlaceAccount

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class TestWorkflow(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.set_up_place_admin()
        PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        self.browser.get(self.live_server_url)
        self.do_logon()

    def test_login(self):
        self.assertTrue(self.check_if_logged_in())

    def test_start_site(self):
        """ standard list view"""
        self.assertTrue(self.check_if_logged_in())
        self.assertTrue(self.browser.find_element_by_id('id_place_list'))
        self.assertTrue(self.browser.find_element_by_id(f'id_place_card_{self.last_place_id}'))

    def test_place_admin_screen(self):
        self.assertTrue(self.check_if_logged_in())
        self.goto_admin_area()
        self.assertTrue(self.wait_for_find_element_by_id('id_place_admin_list', raise_exception=False))

    def test_update_place(self):
        self.assertTrue(
            self.edit_action('id_detail_action_update_place', 'id_who_lives_here', 'id_create_place_submit'))

    def test_update_address(self):
        self.assertTrue(self.edit_action('id_detail_action_update_place_address', 'id_name'))

    def test_add_price(self):
        self.assertTrue(self.edit_action('id_detail_action_create_price', 'id_description'))

    def test_change_price(self):
        self.assertTrue(self.edit_change_action(edit_field=f'id_edit_place_price_{self.last_price_id}',
                                                change_field='id_description'))

    def test_delete_price(self):
        self.assertTrue(self.edit_change_action(edit_field=f'id_delete_place_price_{self.last_price_id}'))

    def test_add_room(self):
        self.assertTrue(self.edit_action('id_detail_action_create_room', 'id_room_number'))

    def test_change_room(self):
        self.assertTrue(self.edit_change_action(edit_field=f'id_edit_place_room_{self.last_room_id}',
                                                change_field='id_room_number'))

    def test_delete_room(self):
        self.assertTrue(self.edit_change_action(edit_field=f'id_delete_place_room_{self.last_room_id}'))

    @skipIf(True, 'not yet implemented')
    def test_add_admin(self):
        self.goto_admin_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_change_admin(self):
        self.goto_admin_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_admin(self):
        self.goto_admin_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_save_changes(self):
        self.goto_admin_area()
        pass

    def goto_admin_area(self):
        pass

    def edit_action(self, action: str, edit_field: str, submit: str = 'id_create_detail_submit') -> bool:
        try:
            element = self._prepare_edit(action=action, edit_field=edit_field)
            element.send_keys('nobody')
        except ValueError:
            return False
        submit_button = self.browser.find_element_by_id(submit)
        submit_button.click()
        return self.is_detail_block()

    def edit_change_action(self, edit_field: str, change_field: str = None) -> bool:
        try:
            element = self._prepare_edit(action='id_detail_action_update_place', edit_field=edit_field)
            element.click()
        except ValueError:
            return False
        if change_field is None:  # means delete
            try:
                self.browser.find_element_by_id(edit_field)
                return False
            except NoSuchElementException:
                return self.wait_for_find_element_by_id('id_create_place_submit', raise_exception=False)
        element2: WebElement = self.wait_for_find_element_by_id(change_field)
        if not isinstance(element2, WebElement):
            logger.warning(f'fetched by {change_field} element is not a web element')
            return False
        element2.send_keys('nobody')
        change_button = self.browser.find_element_by_id('id_create_detail_submit')
        if not isinstance(change_button, WebElement):
            logger.warning('fetched by id_create_detail_submit element is not a web element')
            return False
        change_button.click()
        return self.wait_for_find_element_by_id('id_create_place_submit', raise_exception=False)

    def _prepare_edit(self, action: str, edit_field: str):
        self.assertTrue(self.check_if_logged_in())
        self.goto_admin_area()
        self.assertTrue(self.can_open_detail())
        change_button = self.wait_for_find_element_by_id(action)
        change_button.click()
        # check just one item in the edit screen
        element = self.wait_for_find_element_by_id(edit_field)
        if not isinstance(element, WebElement):
            logger.warning(f'fetched by {edit_field} element is not a web element')
            raise ValueError
        if 'HOST THE WAY' not in self.browser.title:
            logger.warning('title of page is not HOST THE WAY')
            raise ValueError
        return element
