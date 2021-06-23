from django.contrib.auth.models import User
from games.models import Team, Season, Game
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class SeasonGamesApiTestCase(APITestCase):
    def setUp(self):
        self.season = Season.objects.create(name='2020-2021')
        self.team_one = Team.objects.create(name='Team One')
        self.team_two = Team.objects.create(name='Team Two')
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two, season=self.season)
        response = self.client.get('/api/seasons/{}/games/'.format(self.season.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_show(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two, season=self.season)
        response = self.client.get('/api/seasons/{}/games/{}/'.format(self.season.id, game.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], game.id)
        self.assertEqual(response.data['period'], '1')
    
    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        response = self.client.post('/api/seasons/{}/games/'.format(self.season.id), data={'start_time':'01:00:00', 'start_date':'2021-01-01', 'period':'1', 'home_team': self.team_one.id,
                                   'away_team':self.team_two.id, 'season_id':self.season.id, 'home_team_score': 1, 'away_team_score': 2}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['period'], '1')
    
    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two, season=self.season)
        response = self.client.patch('/api/seasons/{}/games/{}/'.format(self.season.id, game.id), data={'period': 'OT'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['period'], 'OT')

    def test_destroy(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two, season=self.season)
        response = self.client.delete('/api/seasons/{}/games/{}/'.format(self.season.id, game.id), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.season.games_count(), 0)
    
    def test_write_fails_without_token(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two, season=self.season)
        response = self.client.patch('/api/seasons/{}/games/{}/'.format(self.season.id, game.id), data={'period': 'OT'}, format='json')
        self.assertEqual(response.status_code, 401)
