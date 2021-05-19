# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from games.models import Game, Team
from games.serializers import GameSerializer, TeamSerializer
from games.throttle import ApiThrottle


class GameViewSet(viewsets.ModelViewSet):
    """
    Hockey games API
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ApiThrottle]


class TeamViewSet(viewsets.ModelViewSet):
    """
    Hockey team API
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ApiThrottle]
