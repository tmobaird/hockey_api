from rest_framework.test import APITestCase

from games.models import Game, Team


class GameApiTestCase(APITestCase):
    def setUp(self):
        self.home_team = Team.objects.create(name="Blackhawks")
        self.away_team = Team.objects.create(name="Maple Leafs")

    def test_index(self):
        Game.objects.create(start='01:00:00', period='1', homeTeam=self.home_team, awayTeam=self.away_team)

        response = self.client.get('/api/games/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_show(self):
        game = Game.objects.create(start='01:00:00', period='1', homeTeam=self.home_team, awayTeam=self.away_team)

        response = self.client.get('/api/games/{}/'.format(game.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)
        self.assertIn('start', response.data)
        self.assertIn('homeTeamScore', response.data)
        self.assertIn('awayTeamScore', response.data)
        self.assertIn('final', response.data)
        self.assertEqual(len(response.data['home'].keys()), 2)
        self.assertIn('id', response.data['home'])
        self.assertIn('name', response.data['home'])
        self.assertEqual(len(response.data['away'].keys()), 2)
        self.assertIn('id', response.data['away'])
        self.assertIn('name', response.data['away'])


class TeamApiTestCase(APITestCase):
    def setUp(self):
        self.team_one = Team.objects.create(name="Blackhawks")
        self.team_two = Team.objects.create(name="Maple Leafs")

    def test_index(self):
        response = self.client.get('/api/teams/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn('id', response.data[0])
        self.assertIn('name', response.data[0])
        self.assertEqual('Blackhawks', response.data[0]['name'])
        self.assertIn('record', response.data[0])

    def test_show(self):
        response = self.client.get('/api/teams/{}/'.format(self.team_one.id), format='json')
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('record', response.data)

    def test_create(self):
        response = self.client.post('/api/teams/', {'name': 'New Team Name'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Team.objects.count(), 3)
        self.assertEqual(Team.objects.latest('id').name, 'New Team Name')

    def test_update(self):
        response = self.client.put('/api/teams/{}/'.format(self.team_two.id), {'name': 'Updated Team Name'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(Team.objects.get(pk=self.team_two.id).name, 'Updated Team Name')