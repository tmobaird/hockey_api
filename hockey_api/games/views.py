from django.http import HttpResponse


# Create your views here.
from rest_framework import viewsets

from games.models import Game
from games.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    Something goes here
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer