from hockey_api.view_helpers import RoadmapItem
from django.http.response import HttpResponse
from django.shortcuts import render
import os

def home(request):
    roadmap = [
        RoadmapItem('Team API', True, None),
        RoadmapItem('Game API', True, 'Updated Daily'),
        RoadmapItem('Season API', True, None),
        RoadmapItem('Nested Team Games API', True, 'Updated Daily'),
        RoadmapItem('Nested Season Games API', True, 'Updated Daily'),
        RoadmapItem('Players API', True, None),
        RoadmapItem('Nested Team Players API', True, None),
        RoadmapItem('Player Stats', False, None),
        RoadmapItem('Game Events API', False, None),
        RoadmapItem('Advanced Game Stats', False, None),
    ]
    return render(request, 'hockey_api/index.html', {'roadmap': roadmap})

def docs(request):
    insomnia_file_url = os.environ.get('INSOMNIA_FILE_URL')
    return render(request, 'hockey_api/docs.html', {'insomnia_file_url': insomnia_file_url})
