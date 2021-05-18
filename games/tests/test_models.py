from django.test import TestCase

# Create your tests here.
from games.models import Team, Game


class GameTestCase(TestCase):
    def test_something(self):
        self.assertEqual(1, 1)


class TeamTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team')
        self.other_team = Team.objects.create(name='Other Team')

    def test_record_losses(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=True, period='F', away_team_score=1,
                            home_team_score=3, start='12:00:000')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=1,
                            home_team_score=0, start='12:00:000')
        self.assertEquals('0-2-0', self.team.record())

    def test_record_wins(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=True, period='F', away_team_score=5,
                            home_team_score=3, start='12:00:000')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=3,
                            home_team_score=4, start='12:00:000')
        self.assertEquals('2-0-0', self.team.record())

    def test_record_ties(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=True, period='F', away_team_score=5,
                            home_team_score=5, start='12:00:000')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=3,
                            home_team_score=3, start='12:00:000')
        self.assertEquals('0-0-2', self.team.record())

    def test_record_does_not_include_in_progress_games(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=False, period='3', away_team_score=5,
                            home_team_score=5, start='12:00:000')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=3,
                            home_team_score=3, start='12:00:000')
        self.assertEquals('0-0-1', self.team.record())

    def test__str__(self):
        team = Team.objects.create(name='Team Name')
        self.assertEquals(team.__str__(), 'Team Name')
