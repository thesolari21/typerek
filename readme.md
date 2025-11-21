# Typerek

## Spis treści / Table of contents
* [General info / Informacje o aplikacji](#general-info)
* [Screens / Zrzuty ekranu](#screens)
* [Specs / Technikalia](#specs)
* [Status](#status)
* [Changelog / Lista zmian](#changelog)


## General info
[PL]

Typerek to aplikacja napisana w Django. Dzięki niej możesz rywalizować z znajomymi w obstawianiu meczy. 

W skrócie:
* Administrator dodaje ligi, mecze oraz relacje user-liga.
* Uczestnicy logując się na swoje konta widzą dostępne dla siebie ligi oraz w ich ramach - mecze / pytania do ligi.
* Każdy mecz posiada informacje o dacie, drużynach oraz mnożniku punktów.
* W danym meczu gracz obstawia dokładny wynik oraz extra-bet.
* Po zakończeniu spotkania, admin uzupełnia wyniki.
* W zależności od konfiguracji następuje automatyczne przeliczenie punktów lub ręczne urucuhomienie skryptu przeliczającego przez administratora.
* Punkty można zdobyć za poprawne wytypowanie bramek danej drużyny, ich różnicy, zwycięzcy oraz zakładu specjalnego (extra bet).
* Spotkania o dużej wadze mogą być ustawione przez administratora z mnożnikiem większym niż 1, np x2 , x3.
* Każdy gracz może również skorzytac z 'pewniaczka' który w przypadku poprawnego obstawienia daje kolejne extra punkty (lub odejmuje przy błędzie)
* Każdy gracz ma dostep do szczegółowych wyników, statystyk oraz klasyfikacji.
* Konfiguracja punktacji dostępna z poziomu administratora.

[EN]

Typerek is a web app built with Django that lets you compete with friends by predicting match results.

In short:

* The admin creates leagues, matches, and assigns users to leagues.
* Players log in to see the leagues they belong to, along with the matches and league questions.
* Each match has a date, teams, and a points multiplier.
* Players predict the exact score and place an extra bet for each match.
* After the match, the admin enters the real results.
* Points are then calculated automatically or manually by the admin, depending on the settings.
* You can earn points for guessing the correct score, goal difference, winner, or the extra bet.
* Important matches can have higher multipliers, like x2 or x3.
* Players can also use a “sure bet” for a chance to get bonus points if correct (or lose points if wrong).
* Everyone can view detailed results, stats, and rankings.
* The scoring system can be fully configured by the admin.
	
## Screens

Main

![](https://i.ibb.co/39DK8Bcs/main.png)

Match detail

![](https://i.ibb.co/2Y6qZ3yG/match-detail.png)

League

![](https://i.ibb.co/Cpqh2s3C/league.png)

Edit match

![](https://i.ibb.co/0jNHHyxd/edit-match.png)

## To Do
* Automartyczne uzupełnianie wyników
* Dodatkowy gracz w lidze oparty na SI + punkty za pokonanie SI
* Wprowadzenie pojedynków
* Tutorial na YT
* Forum/chat
	
## Specs
* Przeliczanie punktów za pomocą skryptu w pliku: xcalc.py
* Wysyłka maili z nieobstawionymi meczami za pomocą skryptu w pliku: xnotbet.py
* Przed uruchomieniem aplikacji uzupełnij w tabeli CONF punktację. Wymagane rekordy:
  * max_jokers
  * p_home_score
  * p_away_score
  * p_sum_goals
  * p_result
  * p_extra_bet
  * p_joker
  * p_answer
* Tabela League, pole Status:
  * 0 - nieaktywne
  * 1 - aktywne (wyświetli ligę userowi)
  * 2 - archiwalna (wyświetl ligę userowi, ale nie uwzgledniaj w pokazywaniu na main i powiadomieniach)
* Tabela Matches, Questions, pole Status:
  * 0 - otwarty (pokaże się na liście meczów, mecz NIE zostanie uwzględniony przy przeliczaniu punktów)
  * 1 - zakończony  (pokaże się na liście meczów, mecz zostanie uwzględniony przy przeliczaniu punktów)
* Tabela Bets, Answers pole Status:
  * 0 - user wszedł w dany mecz, ale nie obstawił
  * 1 - user obstawił mecz
  * 2 - skrypt przeliczył punkty dla danego obstawienia
* Tabela Articles, pole Status:
  * 0 - nieaktywny (nie pokazuj)
  * 1 - aktywny (pokazuj)
* Panel redaktora: dostęp tylko osoby z grupą "redaktor"
* Tabela UserLeagues - należy utworzyć relację aby były widoczne dla użytkownika mecze danej ligi

## Instalacja
Wkrótce...


## Status
Prod

## Changelog
# 1.0
* Działająca aplikacja

# 1.1
* skrypt przeliczający punkty
* zaznaczanie innym kolorem meczy które już sie obstawiło

# 2.0
* pytania do ligi
* ukrywanie/pokazywanie obstawionych meczy w menu głównym
* nowy, czytelniejszy layout w match_detail
* nowa tabela z typami innych użytkowników dla danego meczu (kiedy nie można już obstawiać)
* nowa, czytelniejsza klasyfikacja generalna w leagues
* naprawa wielu pomniejszych bugów graficznych
* 100% responsywność
* loginy/dostępy w 1 pliku .env

# 2.1
* reset hasła by email

# 3.0
* Naprawa błędu polegającego na możliwości zmiany typu po rozpoczęciu meczu
* Poprawka klasyfikacji generalnej aby od razu było sortowanie po sumie punktów malejąco
* Wyświetlanie ile wolnych/wykorzystanych pewniaczków ma user w danej lidze
* Dodany moduł redaktora
* Nowy, ładniejszy, responsywny layout
* Dodanie modułu Aktualności
* Zmiana zasad punktowania (z sumy bramek na różnicę bramek)
* Sylwetki typujących
* Informacja o pozycji zajętej/zajmowanej w danej lidze w tabeli przy sylwetce typującego
* Automatyczny mail do graczy z nieobstawionymi meczami
* Poprawka masy mniejszych błędów

# 3.1
* Poprawa literówek, drobnych błędów w: xcalc.py, xnotbet.py, index.html
* Automatyczny mail do graczy z nowymi meczami w lidze do obstawienia
* Dodanie w leagues kolumny z trafionym wynikiem