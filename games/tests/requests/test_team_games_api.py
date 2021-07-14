from django.contrib.auth.models import User
from games.models import Game, Team
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


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
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], game.id)

    def test_index_can_be_filtered_by_start_date(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        game_two = Game.objects.create(start_time='01:00:00', start_date='2021-01-02', period='1',
                                       home_team=self.team_one,
                                       away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/?start_date=2021-01-02'.format(self.team_one.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], game_two.id)

    def test_index_can_be_filtered_by_start_time(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        game_two = Game.objects.create(start_time='02:30:00', start_date='2021-01-01', period='1',
                                       home_team=self.team_one,
                                       away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/?start_time=01:00:00'.format(self.team_one.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], game.id)

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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], game_three.id)

    def test_show(self):
        game = Game.objects.create(start_time='01:00:00', start_date='2021-01-01', period='1', home_team=self.team_one,
                                   away_team=self.team_two)
        response = self.client.get('/api/teams/{}/games/{}/'.format(self.team_one.id, game.id),
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], game.id)
