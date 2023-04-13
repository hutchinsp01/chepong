from typing import Any, cast

from django.urls import reverse
from django.views.generic import CreateView, DetailView

from app.apps.players.models import Player


class PlayerCreateView(CreateView):
    model = Player
    fields = ["username"]
    template_name = "players/player_create.html"

    def get_success_url(self) -> str:
        return reverse("players:player_detail", kwargs={"pk": cast("Player", self.object).pk})


class PlayerDetailView(DetailView):
    model = Player
    template_name = "players/player_detail.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["seasons"] = self.object.seasonplayer_set.all()
        return context
