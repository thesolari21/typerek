# Generated by Django 4.1.7 on 2023-03-29 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typerek', '0005_alter_bets_p_away_score_alter_bets_p_extra_bet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='extra_bet_name',
            field=models.CharField(default='-', max_length=100, null=True),
        ),
    ]