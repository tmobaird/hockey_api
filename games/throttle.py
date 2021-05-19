from rest_framework import throttling

from games.models import ApiRequest


class ApiThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        ApiRequest.objects.create(user_agent=request.META.get('HTTP_USER_AGENT'), host=request.META.get('HTTP_HOST'),
                                  requester_ip=request.META.get('REMOTE_ADDR'), path=request.path,
                                  method=request.method)
        return True
