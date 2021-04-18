from unittest import TestCase

from rgate_app.requestwrapper import requestsWrapper


class requestsWrapperTest(TestCase):
    def test_safe_request(self):
        with self.subTest("Test non existsing url"):
            url = "https:/wedontknowthis/api"
            response, status_code = requestsWrapper().safe_request(url, {}, "get")
            self.assertEqual((response, status_code), (None, None))

        with self.subTest("Test existsing url"):
            url = "https://google.com"
            response, status_code = requestsWrapper().safe_request(url, {}, "get")
            self.assertEqual(status_code, 200)
