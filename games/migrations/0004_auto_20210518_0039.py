# Generated by Django 3.2.2 on 2021-05-18 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20210511_2233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='awayTeam',
            new_name='away_team',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='awayTeamScore',
            new_name='away_team_score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='homeTeam',
            new_name='home_team',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='homeTeamScore',
            new_name='home_team_score',
        ),
    ]