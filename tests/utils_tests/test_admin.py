from tests.base import BaseTest


class AdminSiteTest(BaseTest):

    def test_admin(self):
        self.set_up_staff()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
