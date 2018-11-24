from django.test.utils import skipIf

from tests.functional_tests.base import FunctionalTest


class TestWorkflow(FunctionalTest):
    @skipIf(True, 'not yet implemented')
    def test_login(self):
        self.logon()
        pass

    @skipIf(True, 'not yet implemented')
    def test_start_site(self):
        pass

    @skipIf(True, 'not yet implemented')
    def test_traveller_screen(self):
        self.goto_traveller_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_comment(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_comment(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_comment(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        self.preview_changes()
        pass

    def test_add_book_request(self):
        self.goto_traveller_area()
        self.open_detail()
        pass

    def test_add_logged_book_request(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        pass

    def test_delete_logged_book_request(self):
        self.goto_traveller_area()
        self.open_detail()
        self.logon()
        pass

    def logon(self):
        pass

    def goto_traveller_area(self):
        pass

    def open_detail(self):
        pass

    def preview_changes(self):
        pass
