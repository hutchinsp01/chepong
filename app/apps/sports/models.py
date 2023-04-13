from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=50, unique=True)
    current_season = models.ForeignKey(
        "Season", on_delete=models.SET_NULL, null=True, blank=True, related_name="current_season"
    )
    track_score = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Season(models.Model):
    number = models.IntegerField()
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="seasons")

    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    is_current = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.sport}: Season {self.number}"

    class Meta:
        unique_together = ("number", "sport")


class Game(models.Model):
    date = models.DateTimeField(null=True)

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="games")

    winner_score = models.IntegerField(default=0)
    loser_score = models.IntegerField(default=0)

    winner_mmr_change = models.IntegerField(default=0)
    loser_mmr_change = models.IntegerField(default=0)

    winner = models.ForeignKey("players.SeasonPlayer", on_delete=models.PROTECT, related_name="won_game")
    loser = models.ForeignKey("players.SeasonPlayer", on_delete=models.PROTECT, related_name="lost_game")

    def __str__(self) -> str:
        return f"{self.season}: {self.winner.short_str()} vs {self.loser.short_str()}"

    def date_str(self) -> str:
        if not self.date:
            return ""
        self.date = self.date.astimezone()
        return self.date.strftime("%d %B %I:%M%p")
