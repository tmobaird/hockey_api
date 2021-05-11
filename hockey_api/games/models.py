from django.db import models


class Team(models.Model):
    name = models.CharField(null=False, max_length=240)

    def __str__(self):
        return self.name

    def record(self):
        return '1-1-0'


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
