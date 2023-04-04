from django import forms

from .models import Bets

class BetForm(forms.ModelForm):

    class Meta:
        model = Bets
        fields = ('team_home_score', 'team_away_score', 'extra_bet', 'joker')
        labels = {
            'team_home_score': '',
            'team_away_score': '',
            'extra_bet': '',
            'joker': '',

        }