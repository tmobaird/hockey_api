from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from games.validators import validate_period, validate_event_type


class Team(models.Model):
    name = models.CharField(null=False, max_length=240)

    def __str__(self):
        return self.name

    def outcomes(self, season):
        games = Game.objects.filter(Q(final=True, season=season) & (Q(away_team=self) | Q(home_team=self)))
        results = {'wins': 0, 'losses': 0, 'ties': 0}
        for game in games:
            if game.away_team == self:
                if game.away_team_score < game.home_team_score:
                    results['losses'] += 1
                elif game.away_team_score == game.home_team_score:
                    results['ties'] += 1
                else:
                    results['wins'] += 1
            else:
                if game.home_team_score < game.away_team_score:
                    results['losses'] += 1
                elif game.away_team_score == game.home_team_score:
                    results['ties'] += 1
                else:
                    results['wins'] += 1
        return results

    def record(self):
        outcomes = self.outcomes(Season.current_season())
        return '{}-{}-{}'.format(outcomes['wins'], outcomes['losses'], outcomes['ties'])


class Season(models.Model):
    name = models.CharField(null=False, max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    current = models.BooleanField(default=False, null=False)

    def games(self):
        return Game.objects.filter(season=self)

    def games_count(self):
        return self.games().count()

    @classmethod
    def current_season(cls):
        season, created = cls.objects.get_or_create(current=True, defaults={'name': 'default'})
        return season

    @classmethod
    def current_season_id(cls):
        return cls.current_season().id


class Game(models.Model):
    start_time = models.TimeField()
    start_date = models.DateField()
    home_team_score = models.IntegerField(default=0, null=False)
    away_team_score = models.IntegerField(default=0, null=False)
    final = models.BooleanField(default=False, null=False)
    period = models.TextField(null=False, validators=[validate_period])
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_teams')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_teams')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, default=Season.current_season_id)

    def home(self):
        return self.home_team

    def away(self):
        return self.away_team


class ApiRequest(models.Model):
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    requester_ip = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)


class Player(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class GameEvent(models.Model):
    type = models.CharField(null=False, max_length=50, validators=[validate_event_type])
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False, null=False)
    scorer = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=False, related_name='scorers')
    primary_assister = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True, related_name='primary_assisters')
    secondary_assister = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True, related_name='secondary_assisters')
    created_at = models.DateTimeField(auto_now_add=True)

