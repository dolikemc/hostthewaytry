import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from places.models import Place
from tests.base import RoleMixin

MAX_WAIT = 5


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
        self.last_place_id = place.id

    def tearDown(self):
        self.browser.quit()

    def do_logon(self):
        logon_button = self.browser.find_element_by_id('navigator-login')
        logon_button.click()
        username = self.browser.find_element_by_id('id_email')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys(self.credentials['email'])
        password.send_keys(self.credentials['password'])
        submit_button = self.browser.find_element_by_id('login-form')
        submit_button.submit()

    def wait_for_find_element_by_id(self, tag_id: str):
        start_time = time.time()
        while True:
            try:
                button = self.browser.find_element_by_id(tag_id)
                return button
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    print(self.browser.page_source)
                    raise e
                time.sleep(0.5)
