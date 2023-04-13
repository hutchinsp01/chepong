# Generated by Django 4.1.7 on 2023-03-23 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0002_game_loser_mmr_change_game_winner_mmr_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='loser_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='winner_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sport',
            name='track_score',
            field=models.BooleanField(default=False),
        ),
    ]
