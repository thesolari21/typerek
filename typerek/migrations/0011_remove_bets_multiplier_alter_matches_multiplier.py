# Generated by Django 4.1.7 on 2023-05-07 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typerek', '0010_alter_bets_joker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bets',
            name='multiplier',
        ),
        migrations.AlterField(
            model_name='matches',
            name='multiplier',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
