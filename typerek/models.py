
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Conf(models.Model):
    name = models.CharField(max_length=30)
    value = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"

class League(models.Model):
    name = models.CharField(max_length=30)
    status = models.PositiveIntegerField(default=0, help_text="0 - Nieaktywna, 1 - Aktywna (pokaż userowi)")

    def __str__(self):
        return f"{self.name}"

class Matches(models.Model):
    date = models.DateTimeField()
    team_home_name = models.CharField(max_length=30)
    team_away_name = models.CharField(max_length=30)
    team_home_score = models.PositiveIntegerField(null=True, blank=True)
    team_away_score = models.PositiveIntegerField(null=True, blank=True)
    multiplier = models.IntegerField(default=1)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    extra_bet_name = models.CharField(max_length=100, null=True, blank=True , default= 'Ż. kartki w meczu'  )
    extra_bet_result = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=0, help_text="0 - Otwarty, 1 - Zakończony (uwzg. przy przel.)")

    def __str__(self):
        return f"{self.team_home_name} - {self.team_away_name}"

class Questions(models.Model):
    date = models.DateTimeField()
    question = models.CharField(max_length=30)
    choice_list = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    answer = models.CharField(max_length=30, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=0, help_text="0 - Otwarty, 1 - Zakończony (uwzg. przy przel.)")

    def __str__(self):
        return f"{self.question}"

class Answers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=30)
    p_answer = models.IntegerField(null=True, blank=True , default=0)
    status = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.question_id} "

class Bets(models.Model):
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    team_home_score = models.PositiveIntegerField(null=True )
    team_away_score = models.PositiveIntegerField(null=True )
    extra_bet = models.PositiveIntegerField(null=True, blank=True )
    joker = models.PositiveIntegerField(null=True, default=0)
    p_home_score = models.IntegerField(null=True, blank=True , default=0)
    p_away_score = models.IntegerField(null=True,blank=True , default=0)
    p_sum_goals = models.IntegerField(null=True, blank=True , default=0)
    p_result = models.IntegerField(null=True, blank=True , default=0)
    p_extra_bet = models.IntegerField(null=True, blank=True , default=0)
    p_joker = models.IntegerField(null=True, blank=True , default=0)
    total = models.IntegerField(null=True, blank=True , default=0)
    status = models.IntegerField(null=True, blank=True, default=0, help_text="0 - user wszedl w mecz,ale nie obstawił, 1 - user obstawił, 2 - skrypt przyliczył punkty")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.match_id} "

class UsersLeagues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.league}"
