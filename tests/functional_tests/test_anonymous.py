from selenium.common.exceptions import NoSuchElementException

from places.models import Place
from tests.functional_tests.base import FunctionalTest


class TestWorkflow(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.set_up_anonymous()
        self.browser.get(self.live_server_url)

    def test_set_up(self):
        self.assertEqual(4, Place.objects.all().count())

    def test_login_not_possible(self):
        self.do_logon()
        self.assertFalse(self.check_if_logged_in())

    def test_cannot_change_place(self):
        self.browser.get(self.live_server_url + '/places')
        detail_button = self.get_detail_block()
        detail_button.click()
        with self.assertRaises(NoSuchElementException):
            self.wait_for_find_element_by_id('id_detail_action_update_place')

    def test_start_site(self):
        self.browser.get(self.live_server_url)
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_start_site_index(self):
        self.browser.get(self.live_server_url + '/places')
        self.wait_for_find_element_by_id('id_place_list')
        self.assertTrue(self.browser.find_element_by_id(f'id_place_card_{self.last_place_id}'))
        self.assertTrue(self.browser.find_element_by_id(f'id_place_card_{self.last_place_id - 1}'))
        self.assertTrue(self.browser.find_element_by_id(f'id_place_card_{self.last_place_id - 2}'))
        self.assertTrue(self.browser.find_element_by_id(f'id_place_card_{self.last_place_id - 3}'))
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_show_detail(self):
        self.browser.get(self.live_server_url + '/places')
        card = self.get_detail_block()
        card.click()
        self.wait_for_find_element_by_id('id_place_detail_bar')
        self.assertTrue(self.browser.find_element_by_id('id_place_detail_info'))
        self.assertTrue(self.browser.find_element_by_id('id_book_place'))

    def test_add_book_request(self):
        self.browser.get(self.live_server_url + '/places')
        card = self.get_detail_block()
        card.click()
        self.wait_for_find_element_by_id('id_place_detail_bar')
        book = self.browser.find_element_by_id('id_book_place')
        book.click()
        self.wait_for_find_element_by_id('id_book_email_form')
        self.assertTrue(self.browser.find_element_by_id('id_book_email_from'))
        self.assertTrue(self.browser.find_element_by_id('id_book_email_to'))
        self.assertTrue(self.browser.find_element_by_id('id_book_email_message'))
