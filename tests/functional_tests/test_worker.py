from django.test.utils import skipIf

from tests.functional_tests.base import FunctionalTest


class TestWorkflow(FunctionalTest):
    @skipIf(True, 'not yet implemented')
    def test_login(self):
        self.logon()
        pass

    @skipIf(True, 'not yet implemented')
    def test_start_site(self):
        self.logon()
        pass

    @skipIf(True, 'not yet implemented')
    def test_worker_screen(self):
        self.logon()
        self.goto_worker_area()
        pass

    @skipIf(True, 'not yet implemented')
    def test_create_place(self):
        self.logon()
        self.goto_worker_area()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_create_admin(self):
        self.logon()
        self.goto_worker_area()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_admin(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_comment(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_comment(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_comment(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_add_area_highlite(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_update_area_highlite(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    @skipIf(True, 'not yet implemented')
    def test_delete_area_highlite(self):
        self.logon()
        self.goto_worker_area()
        self.open_detail()
        self.preview_changes()
        pass

    def logon(self):
        pass

    def goto_worker_area(self):
        pass

    def open_detail(self):
        pass

    def preview_changes(self):
        pass
