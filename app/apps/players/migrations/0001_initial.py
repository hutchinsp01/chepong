# Generated by Django 4.1.7 on 2023-03-10 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('games', models.PositiveIntegerField(default=0)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('current_streak_winning', models.BooleanField(default=True)),
                ('max_win_streak', models.PositiveIntegerField(default=0)),
                ('max_loss_streak', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SeasonPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmr', models.IntegerField(default=1000)),
                ('games', models.PositiveIntegerField(default=0)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('current_streak_winning', models.BooleanField(default=True)),
                ('max_win_streak', models.PositiveIntegerField(default=0)),
                ('max_loss_streak', models.PositiveIntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
            ],
        ),
    ]