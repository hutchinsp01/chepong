from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.apps.core.urls")),
    path("sports/", include("app.apps.sports.urls")),
    path("players/", include("app.apps.players.urls")),
]
