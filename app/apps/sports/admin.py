from django.contrib import admin

from .models import Game, Season, Sport

admin.site.register(Sport)
admin.site.register(Season)
admin.site.register(Game)
