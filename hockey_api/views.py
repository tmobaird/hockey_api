from hockey_api.view_helpers import RoadmapItem
from django.http.response import HttpResponse
from django.shortcuts import render

def home(request):
    roadmap = [
        RoadmapItem('Team API', True, None),
        RoadmapItem('Game API', True, 'Updated Daily'),
        RoadmapItem('Season API', True, None),
        RoadmapItem('Nested Team Games API', True, 'Updated Daily'),
        RoadmapItem('Nested Season Games API', True, 'Updated Daily'),
        RoadmapItem('Players API', False, None),
        RoadmapItem('Player Stats', False, None),
        RoadmapItem('Game Events API', False, None),
        RoadmapItem('Advanced Game Stats', False, None),
    ]
    return render(request, 'hockey_api/index.html', {'roadmap': roadmap})
