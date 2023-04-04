# Generated by Django 4.1.7 on 2023-03-13 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UsersLeagues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='typerek.league')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('team_home_name', models.CharField(max_length=30)),
                ('team_away_name', models.CharField(max_length=30)),
                ('team_home_score', models.IntegerField(blank=True, null=True)),
                ('team_away_score', models.IntegerField(blank=True, null=True)),
                ('multiplier', models.IntegerField()),
                ('extra_bet_name', models.CharField(blank=True, max_length=100, null=True)),
                ('extra_bet_result', models.IntegerField(blank=True, null=True)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='typerek.league')),
            ],
        ),
        migrations.CreateModel(
            name='Bets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_home_score', models.IntegerField(null=True)),
                ('team_away_score', models.IntegerField(null=True)),
                ('extra_bet', models.IntegerField(null=True)),
                ('joker', models.IntegerField(default=0, null=True)),
                ('p_home_score', models.IntegerField(blank=True, null=True)),
                ('p_away_score', models.IntegerField(blank=True, null=True)),
                ('p_sum_goals', models.IntegerField(blank=True, null=True)),
                ('p_diff_goals', models.IntegerField(blank=True, null=True)),
                ('p_extra_bet', models.IntegerField(blank=True, null=True)),
                ('multiplier', models.IntegerField(blank=True, null=True)),
                ('p_joker', models.IntegerField(blank=True, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('match_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='typerek.matches')),
                ('user', models.ForeignKey(default='auth.User', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
