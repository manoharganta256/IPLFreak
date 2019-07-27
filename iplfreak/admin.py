from django.contrib import admin
from iplfreak.models import Match, Deliveries, UserProfile


# Register your models here.
admin.site.register(Match)
admin.site.register(Deliveries)
admin.site.register(UserProfile)
