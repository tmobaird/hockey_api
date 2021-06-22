from django.forms.fields import BooleanField
from rest_framework import serializers
from rest_framework.fields import IntegerField, TimeField, DateField

from games.models import Game, Season, Team
from games.validators import validate_period


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'record']
        querySet = Team.objects.all()


class TeamQuickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']
        queryset = Team.objects.all()


class GameSerializer(serializers.HyperlinkedModelSerializer):
    id = IntegerField(label='ID', read_only=True)
    start_time = TimeField(required=True)
    start_date = DateField(required=True)
    home_team_score = IntegerField(required=True)
    away_team_score = IntegerField(required=True)
    period = serializers.CharField(required=True, validators=[validate_period])
    final = serializers.BooleanField(required=False)
    home_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True, write_only=True)
    away_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True, write_only=True)
    home = TeamQuickSerializer(read_only=True)
    away = TeamQuickSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'start_time', 'start_date', 'home_team_score', 'away_team_score', 'home_team', 'away_team',
                  'home', 'away', 'period', 'final']


class SeasonSerializer(serializers.ModelSerializer):
    id = IntegerField(label='ID', read_only=True)
    current = BooleanField(required=True)

    class Meta:
        model = Season
        fields = ['id', 'current', 'games_count']