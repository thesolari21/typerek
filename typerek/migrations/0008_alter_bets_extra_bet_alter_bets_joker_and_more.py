# Generated by Django 4.1.7 on 2023-04-04 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typerek', '0007_alter_matches_extra_bet_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bets',
            name='extra_bet',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bets',
            name='joker',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bets',
            name='team_away_score',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bets',
            name='team_home_score',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='conf',
            name='value',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='league',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='matches',
            name='extra_bet_result',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='multiplier',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='matches',
            name='team_away_score',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='team_home_score',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
