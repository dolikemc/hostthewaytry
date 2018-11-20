import time

from django.contrib.auth.models import User, Permission, Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from places.models import Place
from traveller.models import PlaceAccount

MAX_WAIT = 5


class VisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("geo.prompt.testing", True)
        self.profile.set_preference("geo.prompt.testing.allow", True)
        self.browser = webdriver.Firefox(firefox_profile=self.profile)
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials, is_staff=True, email='a@b.com')
        Place.objects.create(name='Test1', reviewed=True)
        Place.objects.create(name='Test2', latitude=11, longitude=48, reviewed=True)
        Place.objects.create(name='Test3', latitude=11, longitude=48, reviewed=True)
        place = Place.objects.create(name='Test4', latitude=11, longitude=48, reviewed=True)
        self.last_place_id = place.id

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

    def test_cannot_change_place(self):
        self.browser.get(self.live_server_url)
        self.do_logon()
        detail_button = self.wait_for_find_element_by_id('place-card-' + str(self.last_place_id))
        detail_button.click()
        change_button = self.wait_for_find_element_by_id('detail-action-update-place')
        change_button.click()
        self.assertNotIn('HOST THE WAY', self.browser.title)

    def test_can_change_place(self):
        PlaceAccount.objects.create(place_id=self.last_place_id, traveller_id=1)
        permission: Permission = Permission.objects.filter(codename='change_place').first()
        permission_user = Permission.objects.filter(codename__endswith='_user')
        group: Group = Group.objects.create(name='PlaceAdmin')
        group.permissions.add(permission)
        # for perm in permission_user:
        #    group.permissions.add(perm)
        self.user.groups.add(group)
        self.browser.get(self.live_server_url)
        self.do_logon()
        detail_button = self.wait_for_find_element_by_id('place-card-' + str(self.last_place_id))
        detail_button.click()
        change_button = self.wait_for_find_element_by_id('detail-action-update-place')
        change_button.click()
        # check just one item in the edit screen
        self.wait_for_find_element_by_id('id_who_lives_here')
        self.assertIn('HOST THE WAY', self.browser.title)

    def test_can_register_traveller(self):
        self.browser.get(self.live_server_url)
        self.do_logon()
        register_button = self.browser.find_element_by_id('navigator-register-worker')
        register_button.click()
        self.assertIn('Create User', self.browser.title)
        username = self.browser.find_element_by_id('id_username')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        username.send_keys('place-admin')
        password1.send_keys('DodoGaga')
        password2.send_keys('DodoGaga')
        submit = self.wait_for_find_element_by_id('register-submit')
        submit.click()
        submit2 = self.wait_for_find_element_by_id('create-user-submit')
        self.assertIn('HOST THE WAY', self.browser.title)

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
        logout = self.wait_for_find_element_by_id('navigator-logout')
        self.assertTrue(logout)

    def wait_for_find_element_by_id(self, id: str):
        start_time = time.time()
        while True:
            try:
                button = self.browser.find_element_by_id(id)
                return button
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    print(self.browser.page_source)
                    raise e
                time.sleep(0.5)
