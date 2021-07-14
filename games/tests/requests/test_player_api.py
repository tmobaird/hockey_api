from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from games.models import Player, Team, ApiRequest


class PlayerFactory:
    @staticmethod
    def create(attrs=None):
        if attrs is None:
            attrs = {}
        return Player.objects.create(
            first_name=attrs.get('first_name') or 'Factory',
            last_name=attrs.get('last_name') or 'Player',
            position=attrs.get('position') or 'C',
            team=attrs.get('team') or Team.objects.create(name='Dummy')
        )

class PlayerApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        PlayerFactory.create()
        response = self.client.get('/api/players/', format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 1)

    def test_show(self):
        team = Team.objects.create(name='Chicago Blackhawks')
        player = PlayerFactory.create({'first_name': 'Jonathan', 'last_name': 'Toews', 'position':'C', 'team':team})
        response = self.client.get('/api/players/{}/'.format(player.id), format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['id'], player.id)
        self.assertEquals(response.data['first_name'], 'Jonathan')
        self.assertEquals(response.data['last_name'], 'Toews')
        self.assertEquals(response.data['position'], 'C')
        self.assertEquals(response.data['number'], player.number)
        self.assertEquals(response.data['team']['id'], team.id)

    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        team = Team.objects.create(name='Chicago Blackhawks')
        response = self.client.post('/api/players/', {'first_name': 'Patrick', 'last_name': 'Kane', 'position': 'RW', 'number': 88, 'team_id': team.id}, format='json')
        self.assertEquals(response.status_code, 201)
        self.assertEqual(response.data['first_name'], 'Patrick')
        self.assertEqual(response.data['last_name'], 'Kane')
        self.assertEqual(response.data['position'], 'RW')
        self.assertEqual(response.data['team']['id'], team.id)
        self.assertEqual(response.data['team']['name'], team.name)

    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        player = PlayerFactory.create({'first_name': 'Patty', 'last_name': 'Kane', 'position': 'C'})
        response = self.client.patch('/api/players/{}/'.format(player.id), { 'first_name': 'Patrick', 'last_name': 'Kane', 'position': 'RW' }, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['first_name'], 'Patrick')
        self.assertEquals(response.data['last_name'], 'Kane')
        self.assertEquals(response.data['position'], 'RW')

    def test_destroy(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.api_token.key)
        player = PlayerFactory.create()
        response = self.client.delete('/api/players/{}/'.format(player.id), format='json')
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Player.objects.count(), 0)

    def test_write_actions_require_authentication(self):
        response = self.client.post('/api/players/', {}, format='json')
        self.assertEquals(response.status_code, 401)
        player = PlayerFactory.create()
        response = self.client.patch('/api/players/{}/'.format(player.id), {}, format='json')
        self.assertEquals(response.status_code, 401)
        response = self.client.delete('/api/players/{}/'.format(player.id), format='json')
        self.assertEquals(response.status_code, 401)

    def test_requests_create_api_requests(self):
        count = ApiRequest.objects.count()
        self.client.get('/api/players/', format='json')
        self.assertGreater(ApiRequest.objects.count(), count)

    def test_index_is_filterable_by_team(self):
        team = Team.objects.create(name='Team One')
        PlayerFactory.create({'team': team})
        PlayerFactory.create({'team': team})
        team_two = Team.objects.create(name='Team Two')
        PlayerFactory.create({'team': team_two})
        response = self.client.get('/api/players/?team_id={}'.format(team.id), format='json')
        self.assertEquals(len(response.data['results']), 2)
