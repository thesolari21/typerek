from django import forms
from django.db.models import Sum
from .models import Bets
from .models import Answers
from .models import Conf
from .models import Articles
from .models import Matches
from .models import Questions
from .models import Rules
from django.contrib.auth.models import User
from .models import UserProfile
from easymde.fields import EasyMDEEditor
from django.utils.timezone import localtime
from datetime import datetime
from zoneinfo import ZoneInfo
from django.core.exceptions import ValidationError

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

        joker = int(self.cleaned_data['joker'])

        # Wyszukaj wszystkie zakłady użytkownika dla meczów w ramach danej ligi i zsumuj jokery
        used_jokers = Bets.objects.filter(user=self.user, match_id__league=self.league).exclude(joker=None).aggregate(Sum('joker'))['joker__sum'] or 0
        print(used_jokers)

        if used_jokers + joker > max_jokers:
            raise forms.ValidationError(f'Przekroczono limit pewniaczków ({max_jokers}).')
        return joker

    def save(self, commit=True):

        instance = super().save(commit=False)
        instance.status = 1

        if commit:
            instance.save()

        return instance

class AnswerForm(forms.ModelForm):
    answer = forms.ChoiceField(choices=[], label='')

    class Meta:
        model = Answers
        fields = ('answer',)
        labels = {
            'answer': '',
        }

    def __init__(self, *args, **kwargs ):

        self.user = kwargs['initial']['user']
        self.league = kwargs['initial']['league']
        super().__init__(*args, **kwargs)

        # Pobierz możliwe odpowiedzi z pola choice_list i przekształć na listę
        choices = [(choice, choice) for choice in self.instance.question_id.choice_list.split(',')]
        self.fields['answer'].choices = choices

    def save(self, commit=True):

        instance = super().save(commit=False)
        instance.status = 1

        if commit:
            instance.save()

        return instance


class ArticleForm(forms.ModelForm):
    description = forms.CharField(label='Opis', widget=EasyMDEEditor(attrs={'style': 'width: 100%;'}))

    class Meta:
        model = Articles
        fields = ['title', 'description', 'category', 'status', 'image']
        labels = {
            'title': 'Tytuł',
            'description': 'Opis',
            'category': 'Kategoria',
            'status': 'Status',
            'image': 'Obrazek',
        }
        widgets = {
            'description': EasyMDEEditor(),
        }


    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 200 * 1024:
            raise forms.ValidationError("Obrazek nie może być większy niż 200KB.")
        return image

class MatchForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = [
            'date',
            'team_home_name',
            'team_away_name',
            'team_home_score',
            'team_away_score',
            'multiplier',
            'league',
            'extra_bet_name',
            'extra_bet_result',
            'status'

            ]

        labels = {
            'team_home_name': 'Nazwa gospodarz',
            'team_away_name': 'Nazwa gość',
            'team_home_score': 'Bramki gospodarz',
            'team_away_score': 'Bramki gość',
            'multiplier': 'Mnożnik',
            'league': 'Liga',
            'extra_bet_name': 'Szybki strzał',
            'extra_bet_result': 'Szybki strzał wynik',
            'status': 'Status'
        }

        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = [
            'date',
            'question',
            'choice_list',
            'league',
            'answer',
            'status',

            ]

        labels = {
            'date': 'Data',
            'question': 'Pytanie',
            'choice_list': 'Dozwolone odpowiedzi',
            'league': 'Liga',
            'answer': 'Odpowiedź',
            'status': 'Status',

        }

        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }


class RulesForm(forms.ModelForm):
    game_rules = forms.CharField(label='Zasady gry', widget=EasyMDEEditor(attrs={'style': 'width: 100%;'}))
    payment = forms.CharField(label='Płatność', widget=EasyMDEEditor(attrs={'style': 'width: 100%;'}))

    class Meta:
        model = Rules
        fields = ['game_rules', 'payment', 'additional_info']
        labels = {
            'game_rules': 'Zasady gry',
            'payment': 'Płatność',
            'additional_info': 'Dodatkowe info',

        }
        widgets = {
            'game_rules': EasyMDEEditor(),
            'payment': EasyMDEEditor(),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'nottification_articles', 'nottification_not_bet', 'favourite_club', 'short_info', 'bet_tactic', 'birth_year', 'image']
        labels = {
            'nottification_articles': 'Otrzymuj powiadomienia o aktualnościach (musisz podać maila)',
            'nottification_not_bet': 'Otrzymuj powiadomienia o nieobstawionych meczach (musisz podać maila)',
            'favourite_club': 'Ulubiony klub',
            'short_info': 'O Tobie',
            'bet_tactic': 'Typerska dewiza (jak obstawiasz mecze)',
            'birth_year': 'Rok urodzenia',
            'image': 'Twoja grafika'

        }

class PasswordChangeInlineForm(forms.Form):
    old_password = forms.CharField(
        label='Stare hasło',
        widget=forms.PasswordInput,
        required=False
    )
    new_password1 = forms.CharField(
        label='Nowe hasło',
        widget=forms.PasswordInput,
        required=False
    )
    new_password2 = forms.CharField(
        label='Powtórz nowe hasło',
        widget=forms.PasswordInput,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password2', 'Hasła nie są takie same')

        return cleaned_data