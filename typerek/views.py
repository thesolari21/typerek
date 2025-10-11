from django.shortcuts import render, get_object_or_404
from django.db import models
from typerek.models import Matches
from typerek.models import League
from typerek.models import Bets
from typerek.models import UsersLeagues
from typerek.models import Conf
from typerek.models import Questions
from typerek.models import Answers
from typerek.models import Articles
from typerek.models import Rules
from typerek.models import UserProfile
from django.contrib.auth.models import User
from .forms import BetForm, AnswerForm, ArticleForm, MatchForm, QuestionForm, RulesForm, UserProfileForm, UserForm, PasswordChangeInlineForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from django.db.models import Subquery, Sum, OuterRef, Count, Case, When,Value, IntegerField, F, Q, Window
from django.db.models.functions import Coalesce, Rank
from datetime import datetime, time
from django.utils.timezone import localtime, make_aware
from zoneinfo import ZoneInfo
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import markdown
from bs4 import BeautifulSoup
from django.views.decorators.cache import never_cache

# pomocnicza funkcja oczyszczania z markdown
def markdown_to_text(md_text):
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def login_page(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'] ,password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            if request.POST.get('redir'):
                return redirect(f"{request.POST.get('redir')}")
            else:
                return redirect('typerek:match')
        else:
            context['error'] = 'Podane hasĹ‚o lub login sÄ… bĹ‚Ä™dne! Podaj poprawne dane.'
            if request.POST.get('redir'):
                context['next'] = 'Tylko zalogowani uĹĽytkonicy majÄ… dostÄ™p do tej strony! Zaloguj siÄ™.'
                context['nextURL'] = request.GET.get('next')
            return render(request, 'typerekv3/login.html', context)
    else:
        if request.GET.get('next'):
            context['next'] = 'Tylko zalogowani uĹĽytkonicy majÄ… dostÄ™p do tej strony! Zaloguj siÄ™.'
            context['nextURL'] = request.GET.get('next')
        return render(request, 'typerekv3/login.html', context)

def logout_page(request):
    auth.logout(request)
    return redirect('typerek:match')

def rules(request):
    max_jokers = Conf.objects.get(name='max_jokers').value
    p_joker = Conf.objects.get(name='p_joker').value
    p_result = Conf.objects.get(name='p_result').value
    p_sum_goals = Conf.objects.get(name='p_sum_goals').value
    p_away_score = Conf.objects.get(name='p_away_score').value
    p_home_score = Conf.objects.get(name='p_home_score').value
    p_extra_bet = Conf.objects.get(name='p_extra_bet').value
    p_answer = Conf.objects.get(name='p_answer').value

    rules = Rules.objects.first()  # pierwszy rekord z tabeli


    game_rules_html = markdown.markdown(rules.game_rules, extensions=['extra', 'codehilite'])
    payment_html = markdown.markdown(rules.payment, extensions=['extra', 'codehilite'])
    additional_info_html = markdown.markdown(rules.additional_info, extensions=['extra', 'codehilite'])

    return render(request, 'typerekv3/rules.html', {'max_jokers':max_jokers,'p_joker':p_joker, 'p_result':p_result,'p_sum_goals':p_sum_goals, 'p_away_score':p_away_score, 'p_home_score':p_home_score, 'p_answer':p_answer, 'p_extra_bet':p_extra_bet, 'game_rules_html':game_rules_html, 'payment_html':payment_html, 'additional_info':additional_info_html})


@login_required
def edit_rules(request):
    rules = get_object_or_404(Rules, id=1)

    if request.method == 'POST':
        form = RulesForm(request.POST, request.FILES, instance=rules)
        if form.is_valid():
            form.save()
            return redirect('typerek:rules')
    else:
        form = RulesForm(instance=rules)

    return render(request, 'typerekv3/edit_rules.html', {'form': form, 'rules': rules})



#strona glowna, tylko mecze z lig do ktorych przypisany jest user
@never_cache
def match(request):
    leagues = League.objects.all

    try:
        usersleagues = UsersLeagues.objects.select_related('league').filter(user=request.user).filter(league__status=1)
    except TypeError:
        user = 0
        usersleagues = UsersLeagues.objects.all().filter(user=user)

    poland_timezone = ZoneInfo("Europe/Warsaw")
    current_time_in_poland = datetime.now(poland_timezone)

    # aktywne mecze, mozliwe do obstawienia
    matches = Matches.objects.select_related('league').prefetch_related('bets_set').filter(
        league__in=usersleagues.values('league')
    ).filter(date__gte=current_time_in_poland).order_by('date')

    count_not_bet = 0
    # dodaj info o statusie obstawienia danego meczu przez gracza, od razu tez policz te nieobstawione
    for match in matches:
        try:
            bet = Bets.objects.get(match_id=match, user=request.user)
            match.status = bet.status

        except Bets.DoesNotExist:
            match.status = None

        if match.status == 0 or match.status is None:
            count_not_bet += 1

    # spotkanie niemozliwe juz do obstawienia (uplynal czas), ostatnie 3
    matches_ended = (
        Matches.objects.select_related('league')
        .prefetch_related('bets_set')
        .filter(league__in=usersleagues.values('league'))
        .filter(date__lt=current_time_in_poland)
        .order_by('-date')[:3]
    )

    for match in matches_ended:
        try:
            bet = Bets.objects.get(match_id=match, user=request.user)
            match.status = bet.status

        except Bets.DoesNotExist:
            match.status = None


    # to samo dla pytan do ligi
    questions = Questions.objects.select_related('league').prefetch_related('answers_set').filter(
        league__in=usersleagues.values('league')
    ).filter(date__gte=current_time_in_poland).order_by('date')

    for question in questions:
        try:
            answer = Answers.objects.get(question_id=question, user=request.user)
            question.status = answer.status
        except Answers.DoesNotExist:
            question.status = None

    # pobierz ostatnie 3 artykuĹ‚y (lub mniej), wyczysc formatowanie markdown
    articles = list(Articles.objects.filter(status=1).order_by('-update_date')[:3])

    for article in articles:
        article.teaser = markdown_to_text(article.description)[:300]
        article.teaser = article.teaser + "...  -> czytaj dalej"



    return render(request, 'typerekv3/index.html', {'leagues':leagues, 'matches':matches, 'matches_ended':matches_ended, 'questions':questions, 'articles':articles, 'count_not_bet':count_not_bet})

# uzupelnianie swojego typu
@login_required
def match_detail(request, pk, lg):
    match = get_object_or_404(Matches, pk=pk)

    # jeĹ›li nie istnieje jeszcze typ dla danego meczu, utwĂłrz go (pusty) w momencie wejscia
    try:
        bet = Bets.objects.get(match_id=pk, user=request.user.id)
    except Bets.DoesNotExist:
        bet = Bets(match_id=Matches.objects.get(pk=pk), user=User.objects.get(id=request.user.id))
        bet.save()

    league_id = League.objects.get(name=lg)

    # PorĂłwnaj date/godzine meczu z aktualna data/godzina w Polsce
    poland_timezone = ZoneInfo("Europe/Warsaw")
    current_time_in_poland = datetime.now(poland_timezone)

    if localtime(match.date) > current_time_in_poland:
        can_bet = True
    else:
        can_bet = False

    if request.method == "POST":
        if not can_bet:
            return redirect("typerek:match_detail", pk=pk, lg=lg)

        form = BetForm(request.POST, instance=bet, initial={'user': request.user.id, 'league': league_id})

        if form.is_valid():
            bet = form.save(commit=False)
            bet.status = 1
            bet.last_updated = datetime.now(poland_timezone)
            bet.save()
    else:
        form = BetForm( instance=bet, initial={'user': request.user.id, 'league': league_id })


    # Pobierz typy wszystkich graczy (uwzglednij obstawione i przeliczone)
    bet_all_users = Bets.objects.filter(match_id=pk, status__in=[1,2])

    # Policz wszystkie wykorzystane jokery
    used_jokers = Bets.objects.filter(user=request.user.id, match_id__league=league_id).exclude(joker=None).aggregate(Sum('joker'))['joker__sum'] or 0
    max_jokers = Conf.objects.get(name='max_jokers').value

    return render(request, 'typerekv3/match_detail.html', {'match':match , 'bet':bet, 'form': form, 'can_bet':can_bet, 'bet_all_users':bet_all_users, 'lg':lg, 'used_jokers':used_jokers, 'max_jokers':max_jokers } )

# uzupelnianie odpowiedzi na pytanie do ligi
@login_required
def question_detail(request, pk, lg):
    question = get_object_or_404(Questions, pk=pk)

    #tak samo jak w match_detail: utwĂłrz pusty typ kiedy jeszcze nie ma
    try:
        answer = Answers.objects.get(question_id=pk, user=request.user.id)
    except Answers.DoesNotExist:
        answer = Answers(question_id=Questions.objects.get(pk=pk), user=User.objects.get(id=request.user.id))
        answer.save()

    league_id = League.objects.get(name=lg)

    # PorĂłwnaj date/godzine meczu z aktualna data/godzina w Polsce
    poland_timezone = ZoneInfo("Europe/Warsaw")
    current_time_in_poland = datetime.now(poland_timezone)

    if localtime(question.date) > current_time_in_poland:
        can_bet = True
    else:
        can_bet = False

    if request.method == "POST":
        if not can_bet:
            return redirect("typerek:question_detail", pk=pk, lg=lg)

        form = AnswerForm(request.POST, instance=answer, initial={'user': request.user.id, 'league': league_id})

        if form.is_valid():
            answer = form.save(commit=False)
            answer.status = 1
            answer.last_updated = datetime.now(poland_timezone)
            answer.save()
    else:
        form = AnswerForm(instance=answer, initial={'user': request.user.id, 'league': league_id })


    # Pobierz typy wszystkich graczy (uwzglednij obstawione i przeliczone)
    bet_all_users = Answers.objects.filter(question_id=pk, status__in=[1, 2])

    return render(request, 'typerekv3/question_detail.html', {'question':question , 'answer':answer, 'form': form, 'can_bet':can_bet, 'bet_all_users':bet_all_users, 'lg':lg } )

# podsumowanie danej ligi
def league(request, lg):

    matches = Matches.objects.select_related('league').filter(league__name=lg).values('id')

    # Klasyfikacja generalna meczy, uwzglÄ™dnij tylko przeliczone
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


    # Klasyfikacja generalna za pytania, uwzglednij tylko przeliczone
    questions = Questions.objects.select_related('league').filter(league__name=lg).values('id')

    league_overall_answers = Answers.objects.select_related('user').values('user__username').filter(question_id__in=questions.values('pk'),status__in=[2]).annotate(
                                                          sum_answer=Sum('p_answer'),
    )

    # Teraz przeksztaĹ‚Ä‡ odpowiedzi z pytan do slownika
    answers_dict = {entry['user__username']: entry['sum_answer'] for entry in league_overall_answers}

    # A teraz poĹ‚Ä…cz dane, split_data zawiera dane z pytan o meczyk + punkty z odpowiedzi na pytania + sume punktow z obu kategorii
    split_data = []
    for player in league_overall:
        username = player['user__username']
        sum_answer = answers_dict.get(username, 0)
        total = (player['sum_total'] or 0) + (sum_answer or 0)
        player.update({
            'sum_answer': sum_answer,
            'total_split': total
        })
        split_data.append(player)

    # I jeszcze posortuj
    split_data.sort(
        key=lambda x: (
            x['total_split'],
            x['sum_excellent'],
            x['sum_total']
        ),
        reverse=True
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

    return render(request, 'typerekv3/league.html', {'league_data': split_data, 'matches_overall':matches_overall , 'questions_overall':questions_overall , 'lg':lg })

def articles(request):

    # pobierz parametr z adresu URL
    category_name = request.GET.get('category')

    # pobierz aktywne artykuĹ‚y
    articles = Articles.objects.filter(status=1).order_by('-update_date')

    # jeĹĽeli parametr nie jest None, pofiltruj liste artykuĹ‚Ăłw wg podanej kategorii w parametrze
    if category_name:
        articles = articles.filter(category__category=category_name)


    return render(request, 'typerekv3/articles.html', {'articles': articles,'category_name': category_name })

@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Articles, pk=article_id, status=1)

    article_html = markdown.markdown(article.description, extensions=['extra', 'codehilite'])

    return render(request, 'typerekv3/article_detail.html', {'article': article , 'article_html': article_html })

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('typerek:articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'typerekv3/edit_article.html', {'form': form, 'article': article})

@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # jeĹ›li masz pole author
            article.status = 1  # np. aktywny artykuĹ‚
            article.save()
            return redirect('typerek:articles')
    else:
        form = ArticleForm()

    return render(request, 'typerekv3/add_article.html', {'form': form})

@login_required
def list_of_all_matches(request):
    matches = Matches.objects.filter(status=0).order_by('-date')

    return render(request, 'typerekv3/list_of_all_matches.html', {'matches': matches})

@login_required
def edit_match(request, match_id):
    match = get_object_or_404(Matches, id=match_id)

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('typerek:list_of_all_matches')
    else:
        form = MatchForm(instance=match)

    return render(request, 'typerekv3/edit_match.html', {'form': form, 'match': match})

@login_required
def add_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.save()
            return redirect('typerek:list_of_all_matches')
    else:
        form = MatchForm()

    return render(request, 'typerekv3/add_match.html', {'form': form})


@login_required
def list_of_all_questions(request):
    questions = Questions.objects.filter(status=0).order_by('-date')

    return render(request, 'typerekv3/list_of_all_questions.html', {'questions': questions})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Questions, id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('typerek:list_of_all_questions')
    else:
        form = QuestionForm(instance=question)

    return render(request, 'typerekv3/edit_question.html', {'form': form, 'question': question})

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('typerek:list_of_all_questions')
    else:
        form = QuestionForm()

    return render(request, 'typerekv3/add_question.html', {'form': form})


@login_required
def edit_user_profile(request):
    user = request.user

    # Upewniamy siÄ™, ĹĽe profil istnieje (tworzymy go jeĹ›li nie)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeInlineForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()

            # zmiana hasĹ‚a, jeĹ›li podano
            new_password = password_form.cleaned_data.get('new_password1')
            old_password = password_form.cleaned_data.get('old_password')
            if new_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # NIE wylogowuje po zmianie hasĹ‚a
                    messages.success(request, "HasĹ‚o zostaĹ‚o zmienione.")
                else:
                    password_form.add_error('old_password', 'NieprawidĹ‚owe stare hasĹ‚o')
                    return render(request, 'typerekv3/edit_user_profile.html', {
                        'user_form': user_form,
                        'profile_form': profile_form,
                        'password_form': password_form
                    })

            messages.success(request, "Dane profilu zostaĹ‚y zapisane.")
            return redirect('typerek:match')

    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeInlineForm()

    return render(request, 'typerekv3/edit_user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def display_user(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    user_leagues = UsersLeagues.objects.select_related('league').filter(user=user)
    leagues_data = []

    for ul in user_leagues:
        league = ul.league

        # Ranking wszystkich uĹĽytkownikĂłw w tej lidze
        league_users = UsersLeagues.objects.filter(league=league).select_related('user')

        ranking_list = []
        for lu in league_users:
            u = lu.user
            bets_points = Bets.objects.filter(
                user=u,
                match_id__league=league,
                status=2
            ).aggregate(points=Coalesce(Sum('total'), 0))['points']

            answers_points = Answers.objects.filter(
                user=u,
                question_id__league=league,
                status=2
            ).aggregate(points=Coalesce(Sum('p_answer'), 0))['points']

            total_points = bets_points + answers_points
            ranking_list.append({
                'user': u,
                'bets_points': bets_points,
                'answers_points': answers_points,
                'total_points': total_points
            })

        # Sortujemy po total_points malejÄ…co i nadajemy pozycje
        ranking_list.sort(key=lambda x: x['total_points'], reverse=True)
        for idx, r in enumerate(ranking_list, start=1):
            r['position'] = idx

        # Pobieramy dane dla bieĹĽÄ…cego uĹĽytkownika
        user_data = next(r for r in ranking_list if r['user'] == user)

        bets_count = Bets.objects.filter(user=user, match_id__league=league, status=2).count()
        answers_count = Answers.objects.filter(user=user, question_id__league=league, status=2).count()

        league_info = {
            'name': league.name,
            'status': league.status,
            'bets_count': bets_count,
            'bets_points': user_data['bets_points'],
            'answers_count': answers_count,
            'answers_points': user_data['answers_points'],
            'total_points': user_data['total_points'],
            'position': user_data['position'],
            'players_count': len(ranking_list)
        }

        leagues_data.append(league_info)

    return render(request, 'typerekv3/display_user.html', {
        'user': user,
        'user_profile': user_profile,
        'leagues_data': leagues_data
    })
