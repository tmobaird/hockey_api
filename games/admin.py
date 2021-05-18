from django.contrib import admin

# Register your models here.
from games.models import ApiRequest, Game, Team


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
