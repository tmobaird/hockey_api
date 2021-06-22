from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from games.models import Game, Team, Season
from games.tests.test_throttle import ApiThrottleTestHelper


class GameApiTestCase(APITestCase):
    def setUp(self):
        self.home_team = Team.objects.create(name="Blackhawks")
        self.away_team = Team.objects.create(name="Maple Leafs")
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.home_team,
                            away_team=self.away_team)

        response = self.client.get('/api/games/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_show(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.home_team,
                                   away_team=self.away_team)

        response = self.client.get('/api/games/{}/'.format(game.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertIn('start_time', response.data)
        self.assertIn('start_date', response.data)
        self.assertIn('home_team_score', response.data)
        self.assertIn('away_team_score', response.data)
        self.assertIn('final', response.data)
        self.assertIn('period', response.data)
        self.assertEqual(len(response.data['home'].keys()), 2)
        self.assertIn('id', response.data['home'])
        self.assertIn('name', response.data['home'])
        self.assertEqual(len(response.data['away'].keys()), 2)
        self.assertIn('id', response.data['away'])
        self.assertIn('name', response.data['away'])

    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        self.assertEqual(Game.objects.count(), 0)
        response = self.client.post('/api/games/',
                                    {'start_time': '01:00:000', 'start_date': '2021-01-01', 'home_team_score': 0,
                                     'away_team_score': 0,
                                     'home_team': self.home_team.id, 'away_team': self.away_team.id,
                                     'period': 'F', 'final': True}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Game.objects.count(), 1)

    def test_create_game_with_default_season(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        self.assertEqual(Game.objects.count(), 0)
        response = self.client.post('/api/games/',
                                    {'start_time': '01:00:000', 'start_date': '2021-01-01', 'home_team_score': 0,
                                     'away_team_score': 0,
                                     'home_team': self.home_team.id, 'away_team': self.away_team.id,
                                     'period': 'F', 'final': True}, format='json')
        game = Game.objects.get(pk=response.data['id'])
        self.assertIsInstance(game.season, Season)

    def test_create_fails_when_period_is_not_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        self.assertEqual(Game.objects.count(), 0)
        response = self.client.post('/api/games/', {'period': 'BAD PERIOD', 'start': '01:00:000', 'home_team_score': 0,
                                                    'away_team_score': 0,
                                                    'home_team': self.home_team.id, 'away_team': self.away_team.id,
                                                    'final': True}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Period must be valid', str(response.data['period'][0]))
        self.assertEqual(Game.objects.count(), 0)

    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.home_team,
                                   away_team=self.away_team)
        response = self.client.put('/api/games/{}/'.format(game.id),
                                   {'start_time': '01:00:000', 'start_date': '2021-01-01', 'home_team_score': 2,
                                    'away_team_score': 0,
                                    'home_team': self.home_team.id, 'away_team': self.away_team.id,
                                    'period': 'F', 'final': True}, format='json')
        self.assertEqual(response.status_code, 200)
        game = Game.objects.get(pk=game.id)
        self.assertEqual(game.period, 'F')
        self.assertEqual(game.home_team_score, 2)
        self.assertEqual(game.away_team_score, 0)
        self.assertEqual(game.final, True)

    def test_update_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        response = self.client.put('/api/games/99999/',
                                   {'start': '01:00:000', 'home_team_score': 2, 'away_team_score': 0,
                                    'home_team': self.home_team.id, 'away_team': self.away_team.id,
                                    'period': 'F', 'final': True}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_destroy(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.home_team,
                                   away_team=self.away_team)

        response = self.client.delete('/api/games/{}/'.format(game.id), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Game.objects.count(), 0)
        self.assertEqual(Team.objects.count(), 2)

    def test_tracks_api_requests(self):
        ApiThrottleTestHelper.verify_behavior(self, '/api/games/')

    def test_post_fails_when_not_authenticated(self):
        response = self.client.post('/api/games/', {'name': 'New Team Name'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_put_fails_when_not_authenticated(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.home_team,
                                   away_team=self.away_team)
        response = self.client.put('/api/games/{}/'.format(game.id), {'name': 'Updated Team Name'},
                                   format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_fails_when_not_authenticated(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.home_team,
                                   away_team=self.away_team)
        response = self.client.delete('/api/games/{}/'.format(game.id), format='json')
        self.assertEqual(response.status_code, 401)


class TeamApiTestCase(APITestCase):
    def setUp(self):
        self.team_one = Team.objects.create(name="Blackhawks")
        self.team_two = Team.objects.create(name="Maple Leafs")
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        response = self.client.get('/api/teams/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn('id', response.data[0])
        self.assertIn('name', response.data[0])
        self.assertEqual('Blackhawks', response.data[0]['name'])
        self.assertIn('record', response.data[0])

    def test_index_can_be_filtered_by_name(self):
        response = self.client.get('/api/teams/?name=Blackhawks', format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.team_one.id)

    def test_show(self):
        response = self.client.get('/api/teams/{}/'.format(self.team_one.id), format='json')
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('record', response.data)

    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        response = self.client.post('/api/teams/', {'name': 'New Team Name'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Team.objects.count(), 3)
        self.assertEqual(Team.objects.latest('id').name, 'New Team Name')

    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        response = self.client.put('/api/teams/{}/'.format(self.team_two.id), {'name': 'Updated Team Name'},
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(Team.objects.get(pk=self.team_two.id).name, 'Updated Team Name')

    def test_destroy(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        response = self.client.delete('/api/teams/{}/'.format(self.team_one.id), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Team.objects.count(), 1)

    def test_tracks_api_requests(self):
        ApiThrottleTestHelper.verify_behavior(self, '/api/teams/')

    def test_post_fails_when_not_authenticated(self):
        response = self.client.post('/api/teams/', {'name': 'New Team Name'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_put_fails_when_not_authenticated(self):
        response = self.client.put('/api/teams/{}/'.format(self.team_two.id), {'name': 'Updated Team Name'},
                                   format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_fails_when_not_authenticated(self):
        response = self.client.delete('/api/teams/{}/'.format(self.team_one.id), format='json')
        self.assertEqual(response.status_code, 401)


class TeamGamesApiTestCase(APITestCase):
    def setUp(self):
        self.team_one = Team.objects.create(name="Blackhawks")
        self.team_two = Team.objects.create(name="Maple Leafs")
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        Game.objects.create(start_time='02:00:00', start_date='2021-01-01', period='1', home_team=self.team_two,
                            away_team=self.team_one)
        response = self.client.get('/api/teams/{}/games/'.format(self.team_one.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], game.id)
        self.assertEqual(len(response.data), 2)

    def test_index_can_be_filtered_by_start_date(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        game_two = Game.objects.create(start_time='01:00:00', start_date='2021-01-02', period='1',
                                       home_team=self.team_one,
                                       away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/?start_date=2021-01-02'.format(self.team_one.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], game_two.id)

    def test_index_can_be_filtered_by_start_time(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        game_two = Game.objects.create(start_time='02:30:00', start_date='2021-01-01', period='1',
                                       home_team=self.team_one,
                                       away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/?start_time=01:00:00'.format(self.team_one.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], game.id)

    def test_index_can_be_filtered_by_start_date_and_time(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        game_two = Game.objects.create(start_time='02:30:00', start_date='2021-01-01', period='1',
                                       home_team=self.team_one,
                                       away_team=self.team_two)
        game_three = Game.objects.create(start_time='02:30:00', start_date='2021-01-03', period='1',
                                       home_team=self.team_one,
                                       away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/?start_time=02:30:00&start_date=2021-01-03'.format(self.team_one.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], game_three.id)

    def test_show(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/{}/'.format(self.team_one.id, game.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], game.id)

class SeasonApiTestCase(APITestCase):
    def test_index(self):
        response = self.client.get('/api/seasons/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        season = Season.objects.create(name='2020-2021', current=False)
        response = self.client.get('/api/seasons/{}/'.format(season.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], season.id)
        self.assertEqual(response.data['current'], False)
        self.assertEqual(response.data['games_count'], 0)

    def test_create(self):
        response = self.client.post('/api/seasons/', format='json')
        self.assertEqual(response.status_code, 405)

    def test_update(self):
        season = Season.objects.create(name='2020-2021', current=False)
        response = self.client.patch('/api/seasons/{}/'.format(season.id), format='json')
        self.assertEqual(response.status_code, 405)
    
    def test_destroy(self):
        season = Season.objects.create(name='2020-2021', current=False)
        response = self.client.delete('/api/seasons/{}/'.format(season.id), format='json')
        self.assertEqual(response.status_code, 405)
