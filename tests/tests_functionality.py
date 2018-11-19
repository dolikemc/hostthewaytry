import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from places.models import Place

MAX_WAIT = 10


class VisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("geo.prompt.testing", True)
        self.profile.set_preference("geo.prompt.testing.allow", True)
        self.browser = webdriver.Firefox(firefox_profile=self.profile)
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials, is_staff=True, email='a@b.com')
        Place.objects.create(name='Test1')
        Place.objects.create(name='Test2', latitude=11, longitude=48)
        Place.objects.create(name='Test3', latitude=11, longitude=48)
        Place.objects.create(name='Test4', latitude=11, longitude=48)

    def test_set_up(self):
        self.assertEqual(4, Place.objects.all().count())
        self.assertEqual(1, User.objects.filter(is_staff=True).count())

    def test_can_index_places(self):
        self.browser.get(self.live_server_url + '/places')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_index(self):
        self.browser.get(self.live_server_url)
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_logon(self):
        self.browser.get(self.live_server_url)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('navigator-logout')
        self.do_logon()
        self.assertIn('HOST THE WAY', self.browser.title)
        self.assertTrue(self.browser.find_element_by_id('navigator-logout'))

    def test_can_logout(self):
        self.browser.get(self.live_server_url)
        self.do_logon()
        logout_button = self.browser.find_element_by_id('navigator-logout')
        logout_button.click()
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('navigator-logout')

    def tearDown(self):
        self.browser.quit()

    def do_logon(self):
        start_time = time.time()
        logon_button = self.browser.find_element_by_id('navigator-login')
        logon_button.click()
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys(self.credentials['username'])
        password.send_keys(self.credentials['password'])
        submit_button = self.browser.find_element_by_id('login-form')
        submit_button.submit()
        while True:
            try:
                self.browser.find_element_by_id('navigator-logout')
                return
            except (AssertionError, WebDriverException, NoSuchElementException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
