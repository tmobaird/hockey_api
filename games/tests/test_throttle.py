from unittest import TestCase
from unittest.mock import MagicMock

from django.contrib.auth.models import User

from games.models import ApiRequest
from games.throttle import ApiThrottle


class ApiThrottleTestHelper:
    @staticmethod
    def verify_behavior(test_case, route):
        test_case.assertEqual(0, ApiRequest.objects.count())
        test_case.client.get(route, format='json')
        test_case.assertEqual(1, ApiRequest.objects.count())
        test_case.assertEqual(route, ApiRequest.objects.get().path)


class TestApiThrottle(TestCase):
    def test_throttle_creates_a_new_api_request(self):
        subject = ApiThrottle()
        request = MagicMock(
            META={'HTTP_USER_AGENT': 'dummy user agent', 'HTTP_HOST': 'localhost:8000', 'REMOTE_ADDR': '127.0.0.1'},
            path="/path", method="GET", user=None)
        view = MagicMock()

        count = ApiRequest.objects.count()
        subject.allow_request(request, view)

        self.assertEqual(count + 1, ApiRequest.objects.count())

    def test_throttle_creates_api_request_with_attrs(self):
        subject = ApiThrottle()
        request = MagicMock(
            META={'HTTP_USER_AGENT': 'dummy user agent', 'HTTP_HOST': 'localhost:8000', 'REMOTE_ADDR': '127.0.0.1'},
            path="/path", method="GET", user=None)
        view = MagicMock()

        subject.allow_request(request, view)

        api_request = ApiRequest.objects.latest('created_at')
        self.assertEqual('dummy user agent', api_request.user_agent)
        self.assertEqual('127.0.0.1', api_request.requester_ip)
        self.assertEqual('localhost:8000', api_request.host)
        self.assertEqual('/path', api_request.path)
        self.assertEqual('GET', api_request.method)
        self.assertEqual(None, api_request.requester)

    def test_throttle_create_api_request_associated_with_user(self):
        subject = ApiThrottle()
        user = User.objects.create(username='tester', password='password')
        request = MagicMock(
            META={'HTTP_USER_AGENT': 'dummy user agent', 'HTTP_HOST': 'localhost:8000', 'REMOTE_ADDR': '127.0.0.1'},
            path="/path", method="GET", user=user)
        view = MagicMock()

        subject.allow_request(request, view)

        api_request = ApiRequest.objects.latest('created_at')
        self.assertEqual('dummy user agent', api_request.user_agent)
        self.assertEqual('127.0.0.1', api_request.requester_ip)
        self.assertEqual('localhost:8000', api_request.host)
        self.assertEqual('/path', api_request.path)
        self.assertEqual('GET', api_request.method)
        self.assertEqual(user, api_request.requester)
        self.assertEqual(user.id, api_request.requester_id)
