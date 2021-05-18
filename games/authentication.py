from rest_framework.authentication import BaseAuthentication

from games.models import ApiRequest


class ApiUser():
    def __init__(self, ip):
        self.ip = ip


class ApiAuthentication(BaseAuthentication):
    def authenticate(self, request):
        ApiRequest.objects.create(user_agent=request.META.get('HTTP_USER_AGENT'), host=request.META.get('HTTP_HOST'),
                                  requester_ip=request.META.get('REMOTE_ADDR'), path=request.path,
                                  method=request.method)
        return ApiUser('123'), None
