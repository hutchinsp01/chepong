from typing import Any

from django import forms

from app.apps.players.models import SeasonPlayer
from app.apps.sports.models import Game, Season, Sport
from app.apps.sports.services import SeasonService, SportService


class SportCreateForm(forms.ModelForm):
    def save(self, commit: bool = True) -> Sport:
        return SportService().create_sport(self.cleaned_data["name"])

    class Meta:
        model = Sport
        fields = ["name", "track_score"]


class SeasonPlayerCreateForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["season"].widget = forms.HiddenInput()

    def save(self, commit: bool = True) -> SeasonPlayer:
        return SeasonService().add_new_player(season=self.cleaned_data["season"], player=self.cleaned_data["player"])

    class Meta:
        model = SeasonPlayer
        fields = ["player", "season"]


class SeasonUpdateForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["sport"].widget = forms.HiddenInput()

    class Meta:
        model = Season
        fields = ["sport"]


class SeasonPlayerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: SeasonPlayer) -> str:  # type: ignore[override]
        return obj.short_str()


class GameCreateForm(forms.ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["season"].widget = forms.HiddenInput()

        self.fields["winner"] = SeasonPlayerChoiceField(
            queryset=SeasonPlayer.objects.filter(season=self.initial["season"])
        )
        self.fields["loser"] = SeasonPlayerChoiceField(
            queryset=SeasonPlayer.objects.filter(season=self.initial["season"])
        )

        if not self.initial["season"].sport.track_score:
            self.fields["winner_score"].widget = forms.HiddenInput()
            self.fields["loser_score"].widget = forms.HiddenInput()

    def save(self, commit: bool = True) -> Game:
        return SeasonService().add_game(self.instance)

    class Meta:
        model = Game
        fields = ["season", "winner", "loser", "winner_score", "loser_score"]
