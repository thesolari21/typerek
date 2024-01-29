from django.shortcuts import render, get_object_or_404
from django.db import models
from typerek.models import Matches
from typerek.models import League
from typerek.models import Bets
from typerek.models import UsersLeagues
from typerek.models import Conf
from typerek.models import Questions
from typerek.models import Answers
from .forms import BetForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from django.db.models import Sum, OuterRef, Count, Case, When,Value, IntegerField
from datetime import datetime, timezone, timedelta
from django.contrib.auth.models import User

def login_page(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'] ,password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            if request.POST.get('redir'):
                return redirect(f"{request.POST.get('redir')}")
            else:
                return redirect('match')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            if request.POST.get('redir'):
                context['next'] = 'Tylko zalogowani użytkonicy mają dostęp do tej strony! Zaloguj się.'
                context['nextURL'] = request.GET.get('next')
            return render(request, 'typerek/login.html', context)
    else:
        if request.GET.get('next'):
            context['next'] = 'Tylko zalogowani użytkonicy mają dostęp do tej strony! Zaloguj się.'
            context['nextURL'] = request.GET.get('next')
        return render(request, 'typerek/login.html', context)

def logout_page(request):
    auth.logout(request)
    return redirect('match')

def rules(request):
    max_jokers = Conf.objects.get(name='max_jokers').value
    p_joker = Conf.objects.get(name='p_joker').value
    p_result = Conf.objects.get(name='p_result').value
    p_sum_goals = Conf.objects.get(name='p_sum_goals').value
    p_away_score = Conf.objects.get(name='p_away_score').value
    p_home_score = Conf.objects.get(name='p_home_score').value
    p_extra_bet = Conf.objects.get(name='p_extra_bet').value
    p_answer = Conf.objects.get(name='p_answer').value

    return render(request, 'typerek/rules.html', {'max_jokers':max_jokers,'p_joker':p_joker, 'p_result':p_result,'p_sum_goals':p_sum_goals, 'p_away_score':p_away_score, 'p_home_score':p_home_score, 'p_answer':p_answer, 'p_extra_bet':p_extra_bet})

def match(request):
    leagues = League.objects.all

    try:
        usersleagues = UsersLeagues.objects.select_related('league').filter(user=request.user).filter(league__status=1)

    # na wypadek userów niezalogowanych
    except TypeError:
        user = 0
        usersleagues = UsersLeagues.objects.all().filter(user=user)

    # pobierz aktulną datę, dalej pokaz tylko mecze z datą >= dziś
    current_datetime = datetime.now()
    current_date = current_datetime.date()

    matches = Matches.objects.select_related('league').prefetch_related('bets_set').filter(
        league__in=usersleagues.values('league')
    ).filter(date__gte=current_date).order_by('date')

    # dodaj info o statusie obstawienia danego meczu przez gracza
    for match in matches:
        try:
            bet = Bets.objects.get(match_id=match, user=request.user)
            match.status = bet.status
        except Bets.DoesNotExist:
            match.status = None

    # to samo dla pytan do ligi
    questions = Questions.objects.select_related('league').prefetch_related('answers_set').filter(
        league__in=usersleagues.values('league')
    ).filter(date__gte=current_date).order_by('date')

    for question in questions:
        try:
            answer = Answers.objects.get(question_id=question, user=request.user)
            question.status = answer.status
        except Answers.DoesNotExist:
            question.status = None

    return render(request, 'typerek/index.html', {'leagues':leagues, 'matches':matches, 'questions':questions, 'usersleagues':usersleagues})

@login_required
def match_detail(request, pk, lg):
    match = get_object_or_404(Matches, pk=pk)

    # jeśli nie istnieje jeszcze typ dla danego meczu, utwórz go (pusty) w momencie wejscia
    try:
        bet = Bets.objects.get(match_id=pk, user=request.user.id)
    except Bets.DoesNotExist:
        bet = Bets(match_id=Matches.objects.get(pk=pk), user=User.objects.get(id=request.user.id))
        bet.save()

    league_id = League.objects.get(name=lg)

    if request.method == "POST":

        form = BetForm(request.POST, instance=bet, initial={'user': request.user.id, 'league': league_id})

        if form.is_valid():
            bet = form.save(commit=False)
            bet.status = 1
            bet.save()
    else:
        form = BetForm( instance=bet, initial={'user': request.user.id, 'league': league_id })

    # Pobierz aktualną datę i godzinę w UTC+2
    utc_plus_2_timezone = timezone(timedelta(hours=2))
    current_time_utc_plus_2 = datetime.now(utc_plus_2_timezone)

    # Porównaj match.date z aktualnym czasem w UTC+2
    if match.date > current_time_utc_plus_2:
        can_bet = True
    else:
        can_bet = False

    # Pobierz typy wszystkich graczy (uwzglednij obstawione i przeliczone)
    bet_all_users = Bets.objects.filter(match_id=pk, status__in=[1,2])

    return render(request, 'typerek/match_detail.html', {'match':match , 'bet':bet, 'form': form, 'can_bet':can_bet, 'bet_all_users':bet_all_users, 'lg':lg} )


@login_required
def question_detail(request, pk, lg):
    question = get_object_or_404(Questions, pk=pk)

    #tak samo jak w match_detail: utwórz pusty typ kiedy jeszcze nie ma
    try:
        answer = Answers.objects.get(question_id=pk, user=request.user.id)
    except Answers.DoesNotExist:
        answer = Answers(question_id=Questions.objects.get(pk=pk), user=User.objects.get(id=request.user.id))
        answer.save()

    league_id = League.objects.get(name=lg)

    if request.method == "POST":

        form = AnswerForm(request.POST, instance=answer, initial={'user': request.user.id, 'league': league_id})

        if form.is_valid():
            answer = form.save(commit=False)
            answer.status = 1
            answer.save()
    else:
        form = AnswerForm(instance=answer, initial={'user': request.user.id, 'league': league_id })

    # Pobierz aktualną datę i godzinę w UTC+2
    utc_plus_2_timezone = timezone(timedelta(hours=2))
    current_time_utc_plus_2 = datetime.now(utc_plus_2_timezone)

    # Porównaj question.date z aktualnym czasem w UTC+2
    if question.date > current_time_utc_plus_2:
        can_bet = True
    else:
        can_bet = False

    # Pobierz typy wszystkich graczy (uwzglednij obstawione i przeliczone)
    bet_all_users = Answers.objects.filter(question_id=pk, status__in=[1, 2])

    return render(request, 'typerek/question_detail.html', {'question':question , 'answer':answer, 'form': form, 'can_bet':can_bet, 'bet_all_users':bet_all_users, 'lg':lg} )

def league(request, lg):

    matches = Matches.objects.select_related('league').filter(league__name=lg).values('id')

    # Klasyfikacja generalna, uwzględnij tylko przeliczone
    league_overall = Bets.objects.select_related('user').values('user__username').filter(match_id__in=matches.values('pk'),status__in=[2]).annotate(
                                                          sum_sum_goals=Sum('p_sum_goals') + Sum('p_away_score') + Sum('p_home_score') ,
                                                          sum_result=Sum('p_result'),
                                                          sum_extra_bet=Sum('p_extra_bet'),
                                                          sum_joker=Sum('p_joker'),
                                                          count_result=Count('p_result'),
                                                          sum_excellent=Sum(Case(
                                                              When(p_home_score__gt=0, p_away_score__gt=0, then=Value(1)),
                                                              default=Value(0),
                                                              output_field=IntegerField(),
                                                          )),
                                                          sum_total=Sum('total'),
    ).order_by('sum_total')


    # Bliżnicza sekcja dla pytan do ligi. Rozbilem to na 2 (za dużo komplikacji), póżniej w szablonie html sklejam
    questions = Questions.objects.select_related('league').filter(league__name=lg).values('id')

    league_overall_answers = Answers.objects.select_related('user').values('user__username').filter(question_id__in=questions.values('pk'),status__in=[2]).annotate(
                                                          sum_answer=Sum('p_answer'),
    )


    # Lista obstawionych meczy danego gracza w danej lidze
    matches_overall = Bets.objects.select_related('match_id').filter(
    match_id__in=matches.values('pk'),
    user=User.objects.get(id=request.user.id),
    status__in=[1, 2]
    ).values('match_id',
                'match_id__team_home_name',
                'match_id__team_away_name',
                'match_id__team_home_score',
                'match_id__team_away_score',
                'match_id__league',
                'team_home_score',
                'team_away_score',
                'status',
                'joker',
                'total').order_by('match_id__date')

    # Analogicznie do pytan do ligi
    questions_overall = Answers.objects.select_related('question_id').filter(
    question_id__in=questions.values('pk'),
    user=User.objects.get(id=request.user.id),
    status__in=[1, 2]
    ).values('question_id',
                'question_id__question',
                'question_id__answer',
                'question_id__league',
                'answer',
                'status',
                'p_answer').order_by('question_id__date')

    return render(request, 'typerek/league.html', {'league_overall': league_overall, 'league_overall_answers': league_overall_answers, 'matches_overall':matches_overall , 'questions_overall':questions_overall , 'lg':lg})
