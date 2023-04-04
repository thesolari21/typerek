# Generated by Django 4.1.7 on 2023-03-14 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typerek', '0002_alter_bets_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bets',
            name='extra_bet',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bets',
            name='multiplier',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='bets',
            name='status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
