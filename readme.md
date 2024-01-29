# Typerek

## Spis treści / Table of contents
* [General info / Informacje o aplikacji](#general-info)
* [Screens / Zrzuty ekranu](#screens)
* [Specs / Technikalia](#specs)
* [Status](#status)
* [Changelog / Lista zmian](#changelog)


## General info
[PL]

Aplikacja w Django służąca do obstawiania wyników meczy piłkarskich. Pomysł zrodził się z racji braku aplikacji, która w prosty sposób pozwalałaby na wspólną zabawę w typowanie wyników. 

W skrócie:
* Administrator dodaje ligi, mecze oraz relacje user-liga.
* Uczestnicy logując się na swoje konta widzą dostępne ligi oraz w ich ramach - mecze.
* Każdy mecz posiada informacje o dacie, drużynach oraz mnożniku punktów.
* Każdy gracz obstawia wyniki klikając w dane spotkanie.
* Po zakończeniu spotkania, admin uzupełnia wyniki.
* W zależności od konfiguracji następuje automatyczne przeliczenie punktów lub ręczne urucuhomienie skryptu przeliczającego przez administratora.
* Punkty można zdobyć za poprawne wytypowanie bramek danej drużyny, ich sumy, zwycięzcy oraz zakładu specjalnego.
* Spotkania o dużej wadze mogą być ustawione przez administratora z mnożnikiem większym niż 1, np x2 , x3.
* Każdy gracz może również skorzytac z 'pewniaczka' który w przypadku poprawnego obstawienia daje kolejne extra punkty (lub odejmuje przy błędzie)
* Każdy gracz ma dostep do szczegółowych wyników, statystyk oraz klasyfikacji.
* Konfiguracja punktacji dostępna z poziomu administratora.

[EN]

An application in Django designed for betting on the outcomes of football matches. The idea emerged due to the lack of an application that would allow for easy and collaborative prediction of match results.

In summary:

* The administrator adds leagues, matches, and user-league relationships.
* Participants, upon logging into their accounts, can see available leagues and matches within those leagues.
* Each match includes information about the date, teams, and point multiplier.
* Each player predicts match outcomes by clicking on a specific match.
* After the match is concluded, the admin fills in the results.
* Depending on the configuration, automatic point calculation occurs or the admin manually triggers a script for calculation.
* Points can be earned for correctly predicting goals for a specific team, their sum, the winner, and a special bet.
* Matches of greater importance can be set by the administrator with a higher multiplier, e.g., x2, x3.
* Each player can also use a 'sure bet,' which, when predicted correctly, provides additional points (or deducts points for an error).
* Every player has access to detailed results, statistics, and rankings.
* Point scoring configuration is available from the administrator's interface.
	
## Screens

Main

![](https://i.ibb.co/wY8nqT2/main.png)

Match detail

![](https://i.ibb.co/Bqmb2M3/match-detail.png)

League

![](https://i.ibb.co/Y3s9HRY/league.png)

Rules

![](https://i.ibb.co/Q6VqjB7/rules.png)

## To Do
* Dodanie obsługi pytań otwartych / z listy wg innej punktacji (np. Kto wygra MŚ? [Anglia/Polska/Francja/Niemncy] 50 pkt)
* Automatyczne uzupełnianie wyników meczy (np. z livescore)
* Dodanie statystyk oraz szczegółowych informacji o userze
* Dodanie większej personalizacji (motywy kolorystyczne) dla danej ligi
* Reset hasła z poziomu usera
	
## Specs
* Aktualnie przeliczanie za pomocą skryptu w pliku xcalc.py (sonfiguruj dostęp do DB)
* Przed uruchomieniem aplikacji uzupełnij w tabeli CONF punktację, wymagane rekordy:
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
* Tabela Matches, Questions, pole Status:
  * 0 - otwarty (pokaże się na liście meczów, mecz nie zostanie uwzględniony przy przeliczaniu punktów)
  * 1 - zakończony  (pokaże się na liście meczów, mecz zostanie uwzględniony przy pzeliczani punktów)
* Tabela Bets, Answers pole Status:
  * 0 - user wszedł w dany mecz, ale nie obstawił
  * 1 - user obstawił mecz
  * 2 - skrypt przeliczył punkty dla danego obstawienia
* Tabela UserLeagues - należy utworzyć relację aby były widoczne dla użytkownika mecze danej ligi
* Obstawianie możliwe 2h przed rozpoczęciem meczu
* W main user widzi wszystkie mecze >= TODAY()

## Status
Produkcja

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
