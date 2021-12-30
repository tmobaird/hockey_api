from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def setup_api_auth(test_instance, requiring_auth):
    user, api_token = initialize_api_user()
    if test_instance._testMethodName in requiring_auth:
        mock_authentication(api_token, test_instance)


def initialize_api_user():
    user = User.objects.create(username="tester", password="password")
    api_token = Token.objects.create(user=user)
    return user, api_token


def mock_authentication(token, test_instance):
    test_instance.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
