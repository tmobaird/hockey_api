from django.test import TestCase

# Create your tests here.
from games.models import Team


class GameTestCase(TestCase):
    def test_something(self):
        self.assertEqual(1, 1)


class TeamTestCase(TestCase):
    def test_record(self):
        team = Team.objects.create(name='Team Name')
        self.assertEquals(team.record(), '1-1-0')

    def test__str__(self):
        team = Team.objects.create(name='Team Name')
        self.assertEquals(team.__str__(), 'Team Name')
