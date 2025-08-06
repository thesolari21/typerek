#context processor - tutaj wrzucam funkcje ktora zwroci mi
#dane potrzebne do kazdego wiooku = dostep do menu edycyjnego
# oraz lista kategorii atykułów

from .models import UsersLeagues

def user_leagues_and_access(request):
    # Domyślnie: pusta lista
    active_leagues = UsersLeagues.objects.none()
    archived_leagues = UsersLeagues.objects.none()
    access = False

    # Próba pobrania danych ligowych użytkownika
    try:
        if request.user.is_authenticated:
            # Aktywne ligi (status=1)
            active_leagues = UsersLeagues.objects.select_related('league').filter(
                user=request.user,
                league__status=1
            )

            # Archiwalne ligi (status=2)
            archived_leagues = UsersLeagues.objects.select_related('league').filter(
                user=request.user,
                league__status=2
            )
        else:
            # np. ligi domyślne lub pusta lista – zależnie od potrzeb
            active_leagues = UsersLeagues.objects.select_related('league').filter(
                user=0,
                league__status=1
            )
            archived_leagues = UsersLeagues.objects.select_related('league').filter(
                user=0,
                league__status=2
            )
    except Exception:
        # awaryjne zabezpieczenie
        pass

    # Sprawdzenie dostępu edycyjnego (rola 'redaktor')
    if request.user.is_authenticated:
        access = request.user.groups.filter(name='redaktor').exists()

    return {
        'active_leagues': active_leagues,
        'archived_leagues': archived_leagues,
        'access': access
    }