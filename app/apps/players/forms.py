from typing import cast

from django import forms

from app.apps.players.models import Player
from app.apps.players.services import PlayerService


class PlayerCreateForm(forms.ModelForm):
    def save(self, commit: bool = True) -> Player:
        player = cast("Player", super().save(commit=False))
        if commit:
            PlayerService().create_player(player.username)
        return player

    class Meta:
        model = Player
        fields = ["username", "email"]
