#context processor - tutaj wrzucam funkcje ktora zwroci mi
#dane potrzebne do kazdego wiooku = dostep do menu edycyjnego
# oraz lista kategorii atykułów

from .models import UsersLeagues

def user_leagues_and_access(request):
    # Domyślnie: pusta lista
    usersleagues = UsersLeagues.objects.none()
    access = False

    # Próba pobrania danych ligowych użytkownika
    try:
        if request.user.is_authenticated:
            usersleagues = UsersLeagues.objects.select_related('league').filter(
                user=request.user, league__status=1
            )
        else:
            # np. ligi domyślne lub pusta lista – zależnie od potrzeb
            usersleagues = UsersLeagues.objects.filter(user=0, league__status=1)
    except Exception:
        # awaryjne zabezpieczenie
        usersleagues = UsersLeagues.objects.none()

    # Sprawdzenie dostępu edycyjnego (rola 'redaktor')
    if request.user.is_authenticated:
        access = request.user.groups.filter(name='redaktor').exists()

    return {
        'usersleagues': usersleagues,
        'access': access
    }