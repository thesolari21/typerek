from django import forms
from django.db.models import Sum
from .models import Bets
from .models import Conf

class BetForm(forms.ModelForm):
    YES_NO_CHOICES = (
        (0, 'Nie'),
        (1, 'Tak'),
    )

    joker = forms.ChoiceField(choices=YES_NO_CHOICES, label='')

    class Meta:
        model = Bets
        fields = ('team_home_score', 'team_away_score', 'extra_bet', 'joker')
        labels = {
            'team_home_score': '',
            'team_away_score': '',
            'extra_bet': '',
            'joker': '',

        }

    def __init__(self, *args, **kwargs ):

        self.user = kwargs['initial']['user']
        self.league = kwargs['initial']['league']
        super().__init__(*args, **kwargs)

    def clean_joker(self):

        max_jokers = Conf.objects.get(name='max_jokers')
        max_jokers = max_jokers.value
        print(max_jokers)

        joker = int(self.cleaned_data['joker'])

        # Wyszukaj wszystkie zakłady użytkownika dla meczów w ramach danej ligi i zsumuj jokery
        used_jokers = Bets.objects.filter(user=self.user, match_id__league=self.league).exclude(joker=None).aggregate(Sum('joker'))['joker__sum'] or 0
        print(used_jokers)

        if used_jokers + joker > max_jokers:
            raise forms.ValidationError(f'Przekroczono limit jokerów ({max_jokers}).')
        return joker

    def save(self, commit=True):

        instance = super().save(commit=False)
        instance.status = 1

        if commit:
            instance.save()

        return instance