from django.db import models
from django.db.models import Q


class Team(models.Model):
    name = models.CharField(null=False, max_length=240)

    def __str__(self):
        return self.name

    def outcomes(self):
        games = Game.objects.filter(Q(final=True) & (Q(awayTeam=self) | Q(homeTeam=self)))
        results = {'wins': 0, 'losses': 0, 'ties': 0}
        for game in games:
            if game.awayTeam == self:
                if game.awayTeamScore < game.homeTeamScore:
                    results['losses'] += 1
                elif game.awayTeamScore == game.homeTeamScore:
                    results['ties'] += 1
                else:
                    results['wins'] += 1
            else:
                if game.homeTeamScore < game.awayTeamScore:
                    results['losses'] += 1
                elif game.awayTeamScore == game.homeTeamScore:
                    results['ties'] += 1
                else:
                    results['wins'] += 1
        return results

    def record(self):
        outcomes = self.outcomes()
        return '{}-{}-{}'.format(outcomes['wins'], outcomes['losses'], outcomes['ties'])


class Game(models.Model):
    start = models.TimeField()
    homeTeamScore = models.IntegerField(default=0, null=False)
    awayTeamScore = models.IntegerField(default=0, null=False)
    final = models.BooleanField(default=False, null=False)
    period = models.TextField(null=False)
    homeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_teams')
    awayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_teams')

    def home(self):
        return self.homeTeam

    def away(self):
        return self.awayTeam
