from django.urls import path, include
from rest_framework_nested import routers

from . import views
from .views import GameViewSet, SeasonGamesViewSet, TeamGamesViewSet

router = routers.SimpleRouter()

router.register(r'games', views.GameViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'seasons', views.SeasonViewSet)

teams_router = routers.NestedSimpleRouter(router, r'teams', lookup='team')
teams_router.register('games', TeamGamesViewSet, basename='team-games')

seasons_router = routers.NestedSimpleRouter(router, r'seasons', lookup='season')
seasons_router.register('games', SeasonGamesViewSet, basename='season-games')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(teams_router.urls)),
    path('', include(seasons_router.urls))
]