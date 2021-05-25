from django.urls import path, include
from rest_framework_nested import routers

from . import views
from .views import GameViewSet, TeamGamesViewSet

router = routers.SimpleRouter()

router.register(r'games', views.GameViewSet)
router.register(r'teams', views.TeamViewSet)

teams_router = routers.NestedSimpleRouter(router, r'teams', lookup='team')
teams_router.register('games', TeamGamesViewSet, basename='team-games')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(teams_router.urls)),
]