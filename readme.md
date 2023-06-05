# Typerek

## Spis treści / Table of contents
* [General info / Informacje o aplikacji](#general-info)
* [Screens / Zrzuty ekranu](#screens)
* [Specs / Technikalia](#specs)
* [Status](#status)
* [Changelog / Lista zmian](#changelog)


## General info
[PL]

Aplikacja w Django służąca do obstawiania wyników meczy piłkarskich. Pomysł zrodził się z racji braku aplikcji, która w prosty sposób pozwalałaby na wspólną zabawę w typowanie wyników. 

W dużym skrócie:
* Administrator dodaje ligi, mecze oraz relacje user-liga.
* Uczestnicy logując się na swoje konta widzą podpięte ligi oraz dostępne mecze.
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

soon...
	
## Screens

Main

![](https://i.ibb.co/GHXdK4G/1.png)

Match detail

![](https://i.ibb.co/nPQmv61/2.png)

League

![](https://i.ibb.co/SJJ5Mcq/3.png)

## To Do
* Dodanie formularza samodzielnej rejestracji konta przez usera (aktualnie konta zakłada admin)
* Dodanie obsługi pytań otwartych / z listy wg innej punktacji (np. Kto wygra MŚ? [Anglia/Polska/Francja/Niemncy] 50 pkt)
* Automatyczne uzupełnianie wyników meczy (np. z livescore)
* Dodanie statystyk oraz szczegółowych infomracji o userze
* Dodanie większej poersonalizacji (motywy kolorystyczne) dla danej ligi
	
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
* Tabela League, pole Status:
  * 0 - nieaktywne
  * 1 - aktywne (wyświetli ligę userowi)
* Tabela Matches, pole Status:
  * 0 - otwarty (pokaże się na liście meczów, mecz nie zostanie uwzględniony przy przeliczaniu punktów)
  * 1 - zakończony  (pokaże się na liście meczów, mecz zostanie uwzględniony przy pzeliczani punktów)
* Tabela Bets, pole Status:
  * 0 - user wszedł w dany mecz, ale nie obstawił
  * 1 - user obstawił mecz
  * 2 - skrypt przeliczył punkty dla danego obstawienia
* Tabela UserLeagues - należy utworzyć relację aby były widoczne dla użytkownika mecze danej ligi
* Obstawianie możliwe max dzień przed dniem meczu
* W main user widzi wszystkie mecze >= TODAY()

## Status
Produkcja

## Changelog
# 1.0
* Działająca aplikacja

# 1.1
* skrypt przeliczający punkty
* zaznaczanie innym kolorem meczy które już sie obstawiło
