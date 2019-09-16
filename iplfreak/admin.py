from django.contrib import admin
from iplfreak.models import Match, Deliveries, UserProfile


# Register your models here.
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'season', 'team1', 'team2', 'winner', 'venue']


class DeliveriesAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'innings', 'batsman', 'bowler', 'batsman_runs', 'extra_runs', 'player_dismissed']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture']


admin.site.register(Match, MatchAdmin)
admin.site.register(Deliveries, DeliveriesAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
