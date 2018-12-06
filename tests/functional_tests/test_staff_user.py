from tests.functional_tests.base import FunctionalTest


class TestWorkflow(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.set_up_staff()
        self.browser.get(self.live_server_url)
        self.do_logon()

    def test_login(self):
        self.assertTrue(self.check_if_logged_in())

    def test_can_register_traveller(self):
        # PlaceAccount.objects.create(place_id=self.last_place_id, user_id=self.user.id)
        register_button = self.wait_for_find_element_by_id('id_navigator_register_worker')
        register_button.click()
        self.assertIn('Create User - HOST THE WAY', self.browser.title)
        username = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        username.send_keys('place@admin.com')
        password1.send_keys('DodoGaga')
        password2.send_keys('DodoGaga')
        submit = self.wait_for_find_element_by_id('id_register_submit')
        submit.click()
        # sleep(10)
        submit2 = self.wait_for_find_element_by_id('id_create_user_submit')
        self.assertIn('HOST THE WAY', self.browser.title)

    def goto_staff_area(self):
        pass

    def open_detail(self):
        pass

    def preview_changes(self):
        pass
