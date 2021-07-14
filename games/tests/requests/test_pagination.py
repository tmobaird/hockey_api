from rest_framework.test import APITestCase

from games.models import Player
from games.tests.requests.test_player_api import PlayerFactory


class PaginationApiTestCase(APITestCase):
    def test_pagination_limits(self):
        player = PlayerFactory.create()
        PlayerFactory.create()
        response = self.client.get('/api/players/?limit=1', format='json')
        self.assertEquals(len(response.data['results']), 1)
        self.assertEquals(response.data['results'][0]['id'], player.id)
        self.assertEquals(response.data['count'], 2)
        self.assertIsNotNone(response.data['next'])

    def test_pagination_offsets(self):
        PlayerFactory.create()
        player_two = PlayerFactory.create()
        PlayerFactory.create()
        offset = 1
        response = self.client.get('/api/players/?limit=1&offset={}'.format(offset), format='json')
        self.assertEquals(len(response.data['results']), 1)
        self.assertEquals(response.data['results'][0]['id'], player_two.id)
        self.assertIn('offset={}'.format(offset + 1), response.data['next'])
