from django.db.models import Max
from django.db.models.query import QuerySet
from django.utils import timezone

from app.apps.players.models import Player, SeasonPlayer
from app.apps.players.services import MMRCalculator, SeasonPlayerService
from app.apps.sports.models import Game, Season, Sport


class SeasonService:
    def __init__(self) -> None:
        self.game_service = GameService()
        self.season_player_service = SeasonPlayerService()

    def get_current_season(self, sport: Sport) -> Season | None:
        return sport.seasons.filter(is_current=True).first()

    def get_all_current_seasons(self) -> "QuerySet[Season]":
        return Season.objects.filter(is_current=True).annotate(top_mmr=Max("seasonplayer__mmr")).order_by("-top_mmr")

    def get_season(self, pk: int) -> Season:
        return Season.objects.get(pk=pk)

    def create_season(self, sport: Sport, number: int) -> Season:
        if Season.objects.filter(sport=sport, is_current=True).count() > 0:
            raise Exception("There is already a current season for this sport")
        season = Season.objects.create(sport=sport, number=number, is_current=True, start_date=timezone.now())
        return season

    def end_season(self, season: Season) -> None:
        season.end_date = timezone.now()
        season.is_current = False
        season.save()

    def add_new_player(self, season: Season, player: Player) -> SeasonPlayer:
        return self.season_player_service.create_season_player(season=season, player=player)

    def add_game(self, game: Game) -> Game:
        return self.game_service.add_game(game)

    def get_season_leaderboard(self, season: Season) -> "QuerySet[SeasonPlayer]":
        return season.seasonplayer_set.order_by("-mmr")

    def get_season_games(self, season: Season) -> "QuerySet[Game]":
        return season.games.order_by("-date")

    def recalculate_stats(self, season: Season) -> None:
        for season_player in season.seasonplayer_set.all():
            self.season_player_service.reset_season_player(season_player)

        for game in season.games.all().order_by("date"):
            game = self.game_service.recalculate_game(game)
            self.season_player_service.update_season_player_stats(game)


class SportService:
    def __init__(self) -> None:
        self.season_service = SeasonService()

    def create_sport(self, name: str) -> Sport:
        sport = Sport.objects.create(name=name)
        sport.current_season = self.season_service.create_season(sport, 1)
        sport.save()
        return sport

    def end_season(self, sport: Sport) -> Season:
        if sport.current_season is None:
            raise Exception("Sport has no current season")
        self.season_service.end_season(sport.current_season)
        new_season = self.season_service.create_season(sport, sport.current_season.number + 1)
        sport.current_season = new_season
        sport.save()
        return new_season


class GameService:
    def __init__(self) -> None:
        self.season_player_service = SeasonPlayerService()

    def add_game(self, game: Game) -> Game:
        game = self.game_create(game)
        self.season_player_service.update_season_stats(game)
        return game

    def get_mmr_change(self, game: Game) -> tuple[int, int]:
        return MMRCalculator().calculate_mmr_change(game.winner, game.loser)

    def recalculate_game(self, game: Game) -> Game:
        game.winner_mmr_change, game.loser_mmr_change = self.get_mmr_change(game)
        game.save()
        return game

    def game_create(self, game: Game) -> Game:
        if game.season != game.winner.season or game.season != game.loser.season:
            raise Exception("Game and players must be in the same season")
        if game.winner == game.loser:
            raise Exception("Winner and loser cannot be the same player")

        winner_mmr_change, loser_mmr_change = self.get_mmr_change(game)

        return Game.objects.create(
            date=timezone.now(),
            season=game.season,
            winner=game.winner,
            loser=game.loser,
            winner_mmr_change=winner_mmr_change,
            loser_mmr_change=loser_mmr_change,
            winner_score=game.winner_score,
            loser_score=game.loser_score,
        )
