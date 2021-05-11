from django.http import HttpResponse

# Create your views here.
from rest_framework import viewsets

from games.models import Game, Team
from games.serializers import GameSerializer, TeamSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    Something goes here
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    Hockey team API
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer