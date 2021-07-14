from django.contrib.auth.models import User
from games.models import Team
from games.tests.test_throttle import ApiThrottleTestHelper
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class TeamFactory:
    @staticmethod
    def create(attrs=None):
        if attrs is None:
            attrs = {}
        return Team.objects.create(name=attrs.get('name') or 'Team Name')


class TeamApiTestCase(APITestCase):
    def setUp(self):
        self.team_one = Team.objects.create(name="Blackhawks")
        self.team_two = Team.objects.create(name="Maple Leafs")
        self.user = User.objects.create(username="tester", password="password")
        self.api_token = Token.objects.create(user=self.user)

    def test_index(self):
        response = self.client.get('/api/teams/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('id', response.data['results'][0])
        self.assertIn('name', response.data['results'][0])
        self.assertEqual('Blackhawks', response.data['results'][0]['name'])
        self.assertIn('record', response.data['results'][0])

    def test_index_can_be_filtered_by_name(self):
        response = self.client.get('/api/teams/?name=Blackhawks', format='json')
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.team_one.id)

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
