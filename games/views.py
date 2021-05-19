# Create your views here.
from rest_framework import viewsets

from games.authentication import ApiAuthentication
from games.models import Game, Team
from games.serializers import GameSerializer, TeamSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    Hockey games API
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    authentication_classes = [ApiAuthentication]


class TeamViewSet(viewsets.ModelViewSet):
    """
    Hockey team API
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [ApiAuthentication]
