from app.apps.players.models import Player, SeasonPlayer
from app.apps.sports.models import Game, Season


class PlayerService:
    def create_player(self, username: str) -> Player:
        player = Player.objects.create(username=username)
        return player

    def update_player_stats(self, player: Player, win: bool) -> None:
        player.games += 1

        if win == player.current_streak_winning:
            player.current_streak += 1
        else:
            player.current_streak = 1
        player.current_streak_winning = win

        if win:
            player.wins += 1
            player.max_win_streak = max(player.max_win_streak, player.current_streak)
        else:
            player.losses += 1
            player.max_loss_streak = max(player.max_loss_streak, player.current_streak)

        player.save()


class SeasonPlayerService:
    def create_season_player(self, season: Season, player: Player) -> SeasonPlayer:
        season_player = SeasonPlayer.objects.create(player=player, season=season)
        return season_player

    def reset_season_player(self, season_player: SeasonPlayer) -> None:
        season_player.mmr = 1000
        season_player.games = 0
        season_player.wins = 0
        season_player.losses = 0
        season_player.current_streak = 0
        season_player.current_streak_winning = False
        season_player.max_win_streak = 0
        season_player.max_loss_streak = 0
        season_player.save()

    def update_season_player_stats(self, game: Game) -> None:
        self._update_season_player_stats(game.winner, True, game.winner_mmr_change)
        self._update_season_player_stats(game.loser, False, game.loser_mmr_change)

    def update_player_stats(self, game: Game) -> None:
        player_service = PlayerService()
        player_service.update_player_stats(game.winner.player, True)
        player_service.update_player_stats(game.loser.player, False)

    def update_season_stats(self, game: Game) -> None:
        self.update_season_player_stats(game)
        self.update_player_stats(game)

    def _update_season_player_stats(self, player: SeasonPlayer, win: bool, mmr_change: int) -> None:
        player.mmr += mmr_change
        player.games += 1

        if win == player.current_streak_winning:
            player.current_streak += 1
        else:
            player.current_streak = 1
        player.current_streak_winning = win

        if win:
            player.wins += 1
            player.max_win_streak = max(player.max_win_streak, player.current_streak)
        else:
            player.losses += 1
            player.max_loss_streak = max(player.max_loss_streak, player.current_streak)

        player.save()


class MMRCalculator:
    MAX_ELO_K_FACTOR = 44
    MIN_ELO_K_FACTOR = 26
    GAMES_TO_SETTLE = 20

    def calculate_mmr_change(self, winner: SeasonPlayer, loser: SeasonPlayer) -> tuple[int, int]:
        mmr_adjustment = self._mmr_adjustment(winner.mmr, loser.mmr)
        winner_mmr_change = self._calculate_winner_mmr_change(winner, mmr_adjustment)
        loser_mmr_change = self._calculate_loser_mmr_change(loser, mmr_adjustment)
        return winner_mmr_change, loser_mmr_change

    def _calculate_loser_mmr_change(self, loser: SeasonPlayer, adjustment: float) -> int:
        kf = self._calculate_mmr_k_factor(loser.games + 1)
        return int(-(kf * adjustment))

    def _calculate_winner_mmr_change(self, winner: SeasonPlayer, adjustment: float) -> int:
        kf = self._calculate_mmr_k_factor(winner.games + 1)
        return int(kf * adjustment)

    def _calculate_mmr_k_factor(self, total_games: int) -> float:
        kf_mobility = (self.MAX_ELO_K_FACTOR - self.MIN_ELO_K_FACTOR) / self.GAMES_TO_SETTLE
        return float(max(self.MAX_ELO_K_FACTOR - kf_mobility * total_games, self.MIN_ELO_K_FACTOR))

    def _mmr_adjustment(self, winner_mmr: int, loser_mmr: int) -> float:
        w_tr = 10 ** (winner_mmr / 400)
        l_tr = 10 ** (loser_mmr / 400)
        return float(l_tr / (w_tr + l_tr))
