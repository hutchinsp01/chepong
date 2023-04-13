from django.apps import AppConfig


class PlayersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "app.apps.players"
