from django.shortcuts import render, get_object_or_404
from typerek.models import Matches
from typerek.models import League
from typerek.models import Bets
from typerek.models import UsersLeagues
from typerek.models import Conf
from .forms import BetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from django.db.models import Sum
import datetime
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

    return render(request, 'typerek/rules.html', {'max_jokers':max_jokers,'p_joker':p_joker, 'p_result':p_result,'p_sum_goals':p_sum_goals, 'p_away_score':p_away_score, 'p_home_score':p_home_score, 'p_extra_bet':p_extra_bet})

def match(request):
    leagues = League.objects.all

    try:
        usersleagues = UsersLeagues.objects.select_related('league').filter(user=request.user).filter(league__status=1)
    except TypeError:
        user = 0
        usersleagues = UsersLeagues.objects.all().filter(user=user)

    matches = Matches.objects.select_related('league').prefetch_related('bets_set').filter(
        league__in=usersleagues.values('league')
    ).filter(date__gte=datetime.date.today()).order_by('date')

    for match in matches:
        try:
            bet = Bets.objects.get(match_id=match, user=request.user)
            match.status = bet.status
        except Bets.DoesNotExist:
            match.status = None

    return render(request, 'typerek/index.html', {'leagues':leagues, 'matches':matches, 'usersleagues':usersleagues})

@login_required
def match_detail(request, pk, lg):
    match = get_object_or_404(Matches, pk=pk)

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
        form = BetForm(request.POST, instance=bet, initial={'user': request.user.id, 'league': league_id })


    if match.date > datetime.date.today():
        can_bet = True
    else:
        can_bet = False

    return render(request, 'typerek/match_detail.html', {'match':match , 'bet':bet, 'form': form, 'can_bet':can_bet, 'lg':lg} )


def league(request, lg):

    matches = Matches.objects.select_related('league').filter(league__name=lg).values('id')

    league_overall = Bets.objects.select_related('user').values('user__username').filter(match_id__in=matches.values('pk')).annotate(
                                                          sum_sum_goals=Sum('p_sum_goals') + Sum('p_away_score') + Sum('p_home_score') ,
                                                          sum_result=Sum('p_result'),
                                                          sum_extra_bet=Sum('p_extra_bet'),
                                                          sum_joker=Sum('p_joker'),
                                                          sum_total=Sum('total')).order_by('-sum_total')

    matches_overall = Bets.objects.select_related('match_id').filter(match_id__in=matches.values('pk')).filter(user=User.objects.get(id=request.user.id))\
        .values('match_id',
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

    return render(request, 'typerek/league.html', {'league_overall': league_overall, 'matches_overall':matches_overall , 'lg':lg})
