from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Team(models.Model):
    name = models.CharField(null=False, max_length=240)

    def __str__(self):
        return self.name

    def outcomes(self):
        games = Game.objects.filter(Q(final=True) & (Q(away_team=self) | Q(home_team=self)))
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
        outcomes = self.outcomes()
        return '{}-{}-{}'.format(outcomes['wins'], outcomes['losses'], outcomes['ties'])


class Game(models.Model):
    start = models.TimeField()
    home_team_score = models.IntegerField(default=0, null=False)
    away_team_score = models.IntegerField(default=0, null=False)
    final = models.BooleanField(default=False, null=False)
    period = models.TextField(null=False)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_teams')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_teams')

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
