from games.models import Season
from rest_framework.test import APITestCase


class SeasonApiTestCase(APITestCase):
    def test_index(self):
        response = self.client.get('/api/seasons/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        season = Season.objects.create(name='2020-2021', current=False)
        response = self.client.get('/api/seasons/{}/'.format(season.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], season.id)
        self.assertEqual(response.data['name'], '2020-2021')
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
