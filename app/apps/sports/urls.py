from django.urls import path

from . import views

app_name = 'sports'
urlpatterns = [
    path("", views.SeasonListView.as_view(), name="season_list"),
    path("sport/create/", views.SportCreateView.as_view(), name="create_sport"),
    path("season/<int:pk>/", views.SeasonDetailView.as_view(), name="season_detail"),
    path("season/<int:pk>/games/", views.GameListView.as_view(), name="season_game_list"),
    path("season/<int:pk>/add_player/", views.SeasonPlayerCreateView.as_view(), name="season_player_create"),
    path("season/<int:pk>/add_game", views.GameCreateView.as_view(), name="game_create"),
    path("season/<int:pk>/update/", views.SeasonUpdateView.as_view(), name="season_update"),
    path("season/<int:pk>/end/", views.SeasonEndView.as_view(), name="season_end"),
    path("season/<int:pk>/recalculate/", views.SeasonRecalculateView.as_view(), name="season_recalculate"),

]
