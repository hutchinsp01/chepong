from typing import Any, cast

from django.http import HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from app.apps.players.models import SeasonPlayer
from app.apps.sports.forms import GameCreateForm, SeasonPlayerCreateForm, SeasonUpdateForm, SportCreateForm
from app.apps.sports.models import Game, Season, Sport
from app.apps.sports.services import SeasonService, SportService


class SeasonListView(TemplateView):
    template_name = "sports/season_list.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["seasons"] = SeasonService().get_all_current_seasons()
        return context


class SeasonDetailView(DetailView):
    model = Season
    template_name = "sports/season_detail.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        season = Season.objects.get(pk=self.kwargs["pk"])
        context["season"] = season
        context["leaderboard"] = SeasonService().get_season_leaderboard(season=season)
        return context


class SeasonUpdateView(UpdateView):
    model = Season
    form_class = SeasonUpdateForm
    template_name = "sports/season_update.html"

    def get_success_url(self) -> str:
        return reverse("sports:season_detail", kwargs={"pk": self.object.pk})


class SeasonEndView(UpdateView):
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: dict[str, Any]
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        season = SeasonService().get_season(pk=self.kwargs["pk"])
        new_season = SportService().end_season(season.sport)
        return redirect("sports:season_detail", pk=new_season.pk)


class SeasonRecalculateView(UpdateView):
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: dict[str, Any]
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        season = SeasonService().get_season(pk=self.kwargs["pk"])
        SeasonService().recalculate_stats(season)
        return redirect("sports:season_detail", pk=season.pk)


class SportCreateView(CreateView):
    model = Sport
    form_class = SportCreateForm
    template_name = "sports/sport_create.html"

    def get_success_url(self) -> str:
        sport = cast("Sport", self.object)
        assert sport.current_season
        return reverse("sports:season_detail", kwargs={"pk": sport.current_season.pk})


class SeasonPlayerCreateView(CreateView):
    model = SeasonPlayer
    form_class = SeasonPlayerCreateForm
    template_name = "sports/season_player_create.html"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["season"] = SeasonService().get_season(pk=self.kwargs["pk"])
        return initial

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["season"] = Season.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self) -> str:
        return reverse("sports:season_detail", kwargs={"pk": cast("SeasonPlayer", self.object).season.pk})


class GameCreateView(CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = "sports/game_create.html"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["season"] = SeasonService().get_season(pk=self.kwargs["pk"])
        return initial

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["season"] = Season.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self) -> str:
        return reverse("sports:season_detail", kwargs={"pk": cast("Game", self.object).season.pk})


class GameListView(DetailView):
    model = Season
    template_name = "sports/game_list.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        season_service = SeasonService()
        context = super().get_context_data(**kwargs)
        context["games"] = season_service.get_season_games(season=Season.objects.get(pk=self.kwargs["pk"]))
        return context
