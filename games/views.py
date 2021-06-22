# Create your views here.
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from games.models import Game, Season, Team
from games.serializers import GameSerializer, SeasonSerializer, TeamSerializer
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
    filterset_fields = ['start_date', 'start_time']


class TeamGamesViewSet(GameViewSet):
    def get_queryset(self):
        return Game.objects.filter(Q(away_team=self.kwargs['team_pk']) | Q(home_team=self.kwargs['team_pk']))


class TeamViewSet(viewsets.ModelViewSet):
    """
    Hockey team API
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ApiThrottle]
    filterset_fields = ['name']

class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    NHL Season API
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer