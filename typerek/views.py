from django.shortcuts import render, get_object_or_404
from typerek.models import Matches
from typerek.models import League
from typerek.models import Bets
from typerek.models import UsersLeagues
from .forms import BetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
import datetime

from django.contrib.auth.models import User

# Create your views here.

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

def match(request):
    leagues = League.objects.all

    try:
        usersleagues = UsersLeagues.objects.select_related('league').filter(user=request.user).filter(league__status=1)
    except TypeError:
        user = 0
        usersleagues = UsersLeagues.objects.all().filter(user=user)

    matches = Matches.objects.select_related('league').filter(league__in=usersleagues.values('league')).filter(date__gte=datetime.date.today()).order_by('date')

    return render(request, 'typerek/index.html', {'leagues':leagues, 'matches':matches, 'usersleagues':usersleagues})

@login_required
def match_detail(request, pk, lg):
    match = get_object_or_404(Matches, pk=pk)

    try:
        bet = Bets.objects.get(match_id=pk, user=request.user.id)
    except Bets.DoesNotExist:
        bet = Bets(match_id=Matches.objects.get(pk=pk), user=User.objects.get(id=request.user.id))
        bet.save()


    if request.method == "POST":
        form = BetForm(request.POST, instance=bet)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.status = 1
            bet.save()
    else:
        form = BetForm(instance=bet)

    return render(request, 'typerek/match_detail.html', {'match':match , 'bet':bet, 'form': form} )


def league(request, lg):

    league = UsersLeagues.objects.all()

    return render(request, 'typerek/league.html', {'league': league})
