from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from games.tests.requests.test_player_api import PlayerFactory
from games.tests.requests.test_team_api import TeamFactory


class TeamPlayersApiTestCase(APITestCase):
    def setUp(self):
        self.team = TeamFactory.create()
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        PlayerFactory.create({'team': self.team})
        response = self.client.get('/api/teams/{}/players/'.format(self.team.id), format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)

    def test_show(self):
        player = PlayerFactory.create({'first_name': 'Jonathan', 'last_name': 'Toews', 'position': 'C', 'team': self.team})
        response = self.client.get('/api/teams/{}/players/{}/'.format(self.team.id, player.id), format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['id'], player.id)
        self.assertEquals(response.data['first_name'], 'Jonathan')
        self.assertEquals(response.data['last_name'], 'Toews')
        self.assertEquals(response.data['position'], 'C')
        self.assertEquals(response.data['team']['id'], self.team.id)

    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        response = self.client.post('/api/teams/{}/players/'.format(self.team.id), {'first_name': 'Patrick', 'last_name': 'Kane', 'position': 'RW', 'team_id': self.team.id}, format='json')
        self.assertEquals(response.status_code, 405)

    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        player = PlayerFactory.create({'first_name': 'Patty', 'last_name': 'Kane', 'position': 'C', 'team': self.team})
        response = self.client.patch('/api/teams/{}/players/{}/'.format(self.team.id, player.id),
                                     {'first_name': 'Patrick', 'last_name': 'Kane', 'position': 'RW'}, format='json')
        self.assertEquals(response.status_code, 405)

    def test_destroy(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        player = PlayerFactory.create({'team': self.team})
        response = self.client.delete('/api/teams/{}/players/{}/'.format(self.team.id, player.id), format='json')
        self.assertEquals(response.status_code, 405)
