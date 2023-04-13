from django.urls import path

from . import views

app_name = 'players'
urlpatterns = [
    path("player/create/", views.PlayerCreateView.as_view(), name="player_create"),
    path("player/<int:pk>/", views.PlayerDetailView.as_view(), name="player_detail"),
]
