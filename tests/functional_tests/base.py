import logging
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebElement

from places.models import Place, Room, Price
from tests.base import RoleMixin

MAX_WAIT = 5

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class FunctionalTest(StaticLiveServerTestCase, RoleMixin):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("geo.prompt.testing", True)
        self.profile.set_preference("geo.prompt.testing.allow", True)
        self.browser = webdriver.Firefox(firefox_profile=self.profile)
        Place.objects.create(name='Test1', reviewed=True)
        Place.objects.create(name='Test2', latitude=11, longitude=48, reviewed=True)
        Place.objects.create(name='Test3', latitude=11, longitude=48, reviewed=True)
        place = Place.objects.create(name='Test4', latitude=11, longitude=48, reviewed=True)
        room = Room.objects.create(room_number='01', place_id=place.id)
        price = Price.objects.create(value=2.2, place_id=place.id)
        self.last_price_id = price.id
        self.last_room_id = room.id
        self.last_place_id = place.id

    def tearDown(self):
        self.browser.quit()

    def do_logon(self):

        logon_button = self.browser.find_element_by_id('id_navigator_login')
        logon_button.click()
        username = self.browser.find_element_by_id('id_email')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys(self.credentials['email'])
        password.send_keys(self.credentials['password'])
        submit_button = self.browser.find_element_by_id('id_login_form')
        submit_button.submit()

    def wait_for_find_element_by_id(self, tag_id: str, raise_exception: bool = True):
        return self.wait_for(lambda: self.browser.find_element_by_id(tag_id), raise_exception)

    @staticmethod
    def wait_for(fn, raise_exception: bool = True):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    if raise_exception:
                        raise e
                    else:
                        return False
                time.sleep(0.5)

    def get_detail_block(self, list_id: str) -> WebElement:
        self.wait_for_find_element_by_id(list_id)
        try:
            return self.browser.find_element_by_id(f'id_place_card_{self.last_place_id}')
        except NoSuchElementException:
            return WebElement()

    def is_detail_block(self) -> bool:
        try:
            self.wait_for_find_element_by_id(f"id_place_detail_name")
            return True
        except NoSuchElementException:
            return False

    def can_open_detail(self, list_id: str) -> bool:
        button = self.get_detail_block(list_id)
        button.click()
        return self.is_detail_block()

    def check_if_logged_in(self) -> bool:
        try:
            self.wait_for_find_element_by_id('id_navigator_logout')
            return True
        except NoSuchElementException:
            logger.warning(self.browser.page_source)
            return False
