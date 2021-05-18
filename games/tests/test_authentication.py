from unittest import TestCase
from unittest.mock import MagicMock

from games.authentication import ApiAuthentication
from games.models import ApiRequest


class TestApiAuthentication(TestCase):
    def test_authenticate_creates_a_new_api_request(self):
        subject = ApiAuthentication()
        request = MagicMock(
            META={'HTTP_USER_AGENT': 'dummy user agent', 'HTTP_HOST': 'localhost:8000', 'REMOTE_ADDR': '127.0.0.1'},
            path="/path", method="GET")

        self.assertEqual(0, ApiRequest.objects.count())
        subject.authenticate(request)

        self.assertEqual(1, ApiRequest.objects.count())

    def test_authenticate_creates_api_request_with_attrs(self):
        subject = ApiAuthentication()
        request = MagicMock(
            META={'HTTP_USER_AGENT': 'dummy user agent', 'HTTP_HOST': 'localhost:8000', 'REMOTE_ADDR': '127.0.0.1'},
            path="/path", method="GET")

        subject.authenticate(request)

        api_request = ApiRequest.objects.latest('created_at')
        self.assertEqual('dummy user agent', api_request.user_agent)
        self.assertEqual('127.0.0.1', api_request.requester_ip)
        self.assertEqual('localhost:8000', api_request.host)
        self.assertEqual('/path', api_request.path)
        self.assertEqual('GET', api_request.method)
