from typing import List

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
# Create your tests here.
from games.models import Game, Season, Team


class GameTestCase(TestCase):
    def setUp(self):
        self.home_team = Team.objects.create(name='Home')
        self.away_team = Team.objects.create(name='Away')

    def test_something(self):
        self.assertEqual(1, 1)

    def test_clean_fields_fails_when_period_is_not_allowed_type(self):
        with self.assertRaises(ValidationError):
            game = Game(start_time='10:00.000', start_date='2021-01-01', period='BAD', home_team=self.home_team,
                        away_team=self.away_team)
            game.clean_fields()

    def test_clean_fields_does_not_raise_when_period_is_allowed_type(self):
        try:
            game = Game(start_time='10:00.000', start_date='2021-01-01', period='1', home_team=self.home_team,
                        away_team=self.away_team)
            game.clean_fields()
        except ValidationError:
            self.fail("clean_fields() raised ExceptionType unexpectedly!")

    def test_sets_default_season_when_blank(self):
        game = Game(start_time='10:00.000', start_date='2021-01-01', period='1', home_team=self.home_team,
                    away_team=self.away_team)
        self.assertNotEqual(game.season, None)
        self.assertEquals(game.season.current, True)


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

    def test_record_includes_games_for_current_season(self):
        season, create = Season.objects.get_or_create(current=True, defaults={'name': '2020-2021'})
        team = Team.objects.create(name="Team Name")
        Game.objects.create(away_team=team, home_team=self.other_team, final=True, period='3', away_team_score=5,
                            home_team_score=6, start_time='12:00:000', start_date='2021-01-01', season=season)
        self.assertEquals('0-1-0', team.record())

    def test_record_does_not_include_games_for_non_current_season(self):
        season = Season.objects.create(name='2019-2020', current=False)
        team = Team.objects.create(name='Team Name')
        Game.objects.create(away_team=team, home_team=self.other_team, final=True, period='3', away_team_score=5,
                            home_team_score=6, start_time='12:00:000', start_date='2021-01-01', season=season)
        self.assertEquals('0-0-0', team.record())



class SeasonTestCase(TestCase):
    def setUp(self):
        self.home_team = Team.objects.create(name='Home')
        self.away_team = Team.objects.create(name='Away')

    def test_season_has_games_list(self):
        season = Season.objects.create(name='2020-2021')
        self.assertIsInstance(season.games(), QuerySet)

    def test_season_has_games_list_with_items(self):
        season = Season.objects.create(name='2020-2021')
        Game.objects.create(away_team=self.home_team, home_team=self.away_team, final=True, period='F',
                            away_team_score=1,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01', season=season)
        Game.objects.create(away_team=self.home_team, home_team=self.away_team, final=True, period='F',
                            away_team_score=1,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01', season=season)
        self.assertEquals(len(season.games()), 2)

    def test_season_current_returns_current_season(self):
        Season.objects.all().delete()
        season = Season.objects.create(name='2020-2021', current=True)
        self.assertEqual(Season.current_season_id(), season.id)

    def test_season_current_does_not_return_season_when_false(self):
        Season.objects.all().delete()
        season = Season.objects.create(name='2019-2020', current=False)
        Season.objects.create(name='2020-2021', current=True)
        self.assertNotEqual(Season.current_season_id(), season.id)

    def test_season_games_count_returns_total_number_of_games(self):
        season = Season.objects.create(name='2020-2021')
        Game.objects.create(away_team=self.home_team, home_team=self.away_team, final=True, period='F',
                            away_team_score=1,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01', season=season)
        Game.objects.create(away_team=self.home_team, home_team=self.away_team, final=True, period='F',
                            away_team_score=1,
                            home_team_score=3, start_time='12:00:000', start_date='2021-01-01', season=season)
        self.assertEqual(season.games_count(), 2)

    def test_current_season_returns_season(self):
        Season.objects.all().delete()
        season = Season.objects.create(name='2020-2021', current=True)
        season_two = Season.objects.create(name='2019-2020', current=False)
        self.assertEqual(Season.current_season().id, season.id)
        self.assertNotEqual(Season.current_season().id, season_two.id)
