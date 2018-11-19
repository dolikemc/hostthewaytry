import time
from unittest import TestCase, main

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class VisitorTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.profile = webdriver.FirefoxProfile()
        cls.profile.set_preference("geo.prompt.testing", True)
        cls.profile.set_preference("geo.prompt.testing.allow", True)
        # cls.profile.set_preference('geo.wifi.uri', GEOLOCATION_PATH)
        cls.browser = webdriver.Firefox(firefox_profile=cls.profile)

    def test_can_start(self):
        self.browser.get('http://localhost:8000/places')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_index(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_logon(self):
        self.browser.get('http://localhost:8000')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('navigator-logout')
        logon_button = self.browser.find_element_by_id('navigator-login')
        logon_button.click()
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('christoph')
        password.send_keys('bambi27.')
        submit_button = self.browser.find_element_by_id('login-form')
        submit_button.submit()
        time.sleep(1)
        self.assertIn('HOST THE WAY', self.browser.title)
        self.assertTrue(self.browser.find_element_by_id('navigator-logout'))

    @classmethod
    def tearDown(cls):
        cls.browser.quit()


if __name__ == '__main__':
    main(warnings='ignore')
