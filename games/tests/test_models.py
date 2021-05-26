from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from games.models import Team, Game


class GameTestCase(TestCase):
    def setUp(self):
        self.home_team = Team.objects.create(name='Home')
        self.away_team = Team.objects.create(name='Away')

    def test_something(self):
        self.assertEqual(1, 1)

    def test_clean_fields_fails_when_period_is_not_allowed_type(self):
        with self.assertRaises(ValidationError):
            game = Game(start_time='10:00.000', start_date='2021-01-01', period='BAD', home_team=self.home_team, away_team=self.away_team)
            game.clean_fields()

    def test_clean_fields_does_not_raise_when_period_is_allowed_type(self):
        try:
            game = Game(start_time='10:00.000', start_date='2021-01-01', period='1', home_team=self.home_team, away_team=self.away_team)
            game.clean_fields()
        except ValidationError:
            self.fail("clean_fields() raised ExceptionType unexpectedly!")


class TeamTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team')
        self.other_team = Team.objects.create(name='Other Team')

    def test_record_losses(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=True, period='F', away_team_score=1,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=1,
                            home_team_score=0, start_time='12:00:000', start_date='2021-01-01')
        self.assertEquals('0-2-0', self.team.record())

    def test_record_wins(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=True, period='F', away_team_score=5,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=3,
                            home_team_score=4, start_time='12:00:000', start_date='2021-01-01')
        self.assertEquals('2-0-0', self.team.record())

    def test_record_ties(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=True, period='F', away_team_score=5,
                            home_team_score=5, start_time='12:00:000', start_date='2021-01-01')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=3,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01')
        self.assertEquals('0-0-2', self.team.record())

    def test_record_does_not_include_in_progress_games(self):
        Game.objects.create(away_team=self.team, home_team=self.other_team, final=False, period='3', away_team_score=5,
                            home_team_score=5, start_time='12:00:000', start_date='2021-01-01')
        Game.objects.create(away_team=self.other_team, home_team=self.team, final=True, period='F', away_team_score=3,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01')
        self.assertEquals('0-0-1', self.team.record())

    def test__str__(self):
        team = Team.objects.create(name='Team Name')
        self.assertEquals(team.__str__(), 'Team Name')
