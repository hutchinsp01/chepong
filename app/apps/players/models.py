from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class Player(models.Model):
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    # These are all currently not correct - dont trust
    games = models.PositiveIntegerField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    current_streak = models.PositiveIntegerField(default=0)
    current_streak_winning = models.BooleanField(default=True)

    max_win_streak = models.PositiveIntegerField(default=0)
    max_loss_streak = models.PositiveIntegerField(default=0)

    def get_absolute_url(self) -> str:
        return reverse("players:player_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.username


class SeasonPlayer(models.Model):
    player = models.ForeignKey("players.Player", on_delete=models.CASCADE)
    season = models.ForeignKey("sports.Season", on_delete=models.CASCADE)

    mmr = models.IntegerField(default=1000)

    games = models.PositiveIntegerField(default=0)

    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    current_streak = models.PositiveIntegerField(default=0)
    current_streak_winning = models.BooleanField(default=True)

    # Records
    max_win_streak = models.PositiveIntegerField(default=0)
    max_loss_streak = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.season} - {self.player}"

    @cached_property
    def points_for(self) -> int:
        for_winning = (
            self.season.games.filter(winner=self).aggregate(models.Sum("winner_score"))["winner_score__sum"] or 0
        )
        for_losing = self.season.games.filter(loser=self).aggregate(models.Sum("loser_score"))["loser_score__sum"] or 0
        return for_losing + for_winning

    @cached_property
    def points_against(self) -> int:
        against_winning = (
            self.season.games.filter(winner=self).aggregate(models.Sum("loser_score"))["loser_score__sum"] or 0
        )
        against_losing = (
            self.season.games.filter(loser=self).aggregate(models.Sum("winner_score"))["winner_score__sum"] or 0
        )
        return against_losing + against_winning

    @cached_property
    def points_diff(self) -> int:
        return self.points_for - self.points_against

    @property
    def win_percentage(self) -> str:
        if self.games == 0:
            return "0.00"

        return f"{(self.wins / self.games) * 100:.2f}"

    def short_str(self) -> str:
        return f"{self.player.username}"

    def get_streak_emoji(self) -> str:
        if self.current_streak < 2:
            return ""
        if self.current_streak_winning:
            return "🔥"
        return "🥶"

    def get_absolute_url(self) -> str:
        return reverse("players:player_detail", kwargs={"pk": self.player.pk})

    class Meta:
        unique_together = ("player", "season")
