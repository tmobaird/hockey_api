from django.contrib import admin

# Register your models here.
from games.models import ApiRequest, Game, Team, Season, Player, GameEvent


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'path',
                    'method',
                    'requester',
                    'requester_ip',
                    'user_agent',
                    'created_at')
    list_filter = ('method', 'created_at')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'start_date',
                    'start_time',
                    'home_team_score',
                    'away_team_score',
                    'home_team',
                    'away_team',
                    'final',
                    'period')
    list_filter = ('start_date',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('name', 'created_at')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','number','position','team')
    list_filter = ('position','team')


@admin.register(GameEvent)
class GameEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'game', 'scorer', 'primary_assister', 'secondary_assister', 'created_at')
