from unittest import TestCase

import hosttheway.wsgi as WSGI


class WsgiTest(TestCase):
    def test_wsgi_load(self):
        self.assertTrue(WSGI.get_wsgi_application())
