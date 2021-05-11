from rest_framework import serializers
from rest_framework.fields import IntegerField, TimeField

from games.models import Game, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']
        queryset = Team.objects.all()


class GameSerializer(serializers.HyperlinkedModelSerializer):
    id = IntegerField(label='ID', read_only=True)
    start = TimeField(required=True)
    homeTeamScore = IntegerField(required=True)
    awayTeamScore = IntegerField(required=True)
    homeTeam = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True, write_only=True)
    awayTeam = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True, write_only=True)
    home = TeamSerializer(read_only=True)
    away = TeamSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'start', 'homeTeamScore', 'awayTeamScore', 'homeTeam', 'awayTeam', 'homeTeam', 'awayTeam',
                  'home', 'away']
