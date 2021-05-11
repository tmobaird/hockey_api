from django.db import models


class Game(models.Model):
    start = models.TimeField()
    homeTeamScore = models.IntegerField(default=0,null=False)
    awayTeamScore = models.IntegerField(default=0,null=False)
    final = models.BooleanField(default=False,null=False)
    period = models.TextField(null=False)
