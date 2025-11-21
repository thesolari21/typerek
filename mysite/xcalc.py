import mysql.connector
import os
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def run_sql_statement(sql_statement):
    # Konfiguracja połączenia z bazą danych

    config = {
        'user': env('DATABASE_USER'),
        'password': env('DATABASE_PASS'),
        'host': env('DATABASE_HOST'),
        'database': env('DATABASE_NAME'),
        'raise_on_warnings': True
    }

    try:
        # Utworzenie połączenia z bazą danych
        with mysql.connector.connect(**config) as connection:
            with connection.cursor() as cursor:
                # Podziel zapytanie na poszczególne polecenia
                statements = sql_statement.split(';')

                # Wykonaj poszczególne polecenia
                i = 1
                for statement in statements:
                    if statement.strip():
                        cursor.execute(statement)
                        print("Zapytanie SQL: " + str(i))
                        i = i+1

                connection.commit()

    except mysql.connector.Error as error:
        print("Błąd wykonania wyrażenia SQL:", error)


sql_statement = """

set @p_home_score = (select value from typerek_conf where name = 'p_home_score');
set @p_away_score = (select value from typerek_conf where name = 'p_away_score');
set @p_sum_goals = (select value from typerek_conf where name = 'p_sum_goals');
set @p_result = (select value from typerek_conf where name = 'p_result');
set @p_extra_bet = (select value from typerek_conf where name = 'p_extra_bet');
set @p_joker = (select value from typerek_conf where name = 'p_joker');


update
	typerek_bets tb
    inner join

    (
	select * , ((calc_p_home_score + calc_p_away_score + calc_p_sum_goals + calc_p_result + calc_p_extra_bet + calc_p_joker) * multiplier ) as calc_p_total
	from
	(
	select
	m.status as mstat,              -- match status
	b.status ,                      -- bet status
	b.id ,                          -- bet id
	b.match_id_id ,                 -- match id
	b.user_id ,                     -- user id
	m.multiplier,                   -- multiplier
	m.team_home_score as mths,      -- home score in match
	m.team_away_score as mtas,      -- away score in match
	m.extra_bet_result,             -- etra bet result in match
	b.team_home_score as bths,      -- bet home score
	b.team_away_score as btas,      -- bet away score
	b.extra_bet,                    -- bet extra bet
	b.joker,                        -- bet joket

	CASE                            -- calculate points for home score
		when m.team_home_score = b.team_home_score then @p_home_score
		else 0
	END as 'calc_p_home_score',
	CASE                            -- calculate points for away score
		when m.team_away_score = b.team_away_score then @p_away_score
		else 0
	END as 'calc_p_away_score',
	CASE                            -- calculate points for DIFF goals, change after tests, name of variable non-changed 
		when (CAST(m.team_away_score as signed) - CAST(m.team_home_score as signed))  = (CAST(b.team_away_score as signed) - CAST(b.team_home_score as signed)) then @p_sum_goals
		else 0
	END as 'calc_p_sum_goals',
	CASE                            -- calculate point for result
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) * (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) > 0 then @p_result
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) = (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) then @p_result
		else 0
	END as 'calc_p_result',
	CASE                            -- calculate points for extra bet
		when m.extra_bet_result = b.extra_bet then @p_extra_bet
		else 0
	END as 'calc_p_extra_bet',
	CASE                            -- calculate points for joker
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) * (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) > 0 then @p_joker * b.joker
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) = (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) then @p_joker * b.joker
		else cast(@p_joker as signed) * cast(b.joker as signed) * -1
	END as 'calc_p_joker'

	from typerek_matches m
	inner join typerek_bets b
	on m.id = b.match_id_id and b.status = 1 and m.status = 1   -- must bet status = 1 (bet) and match status = 1 (closed)
	) z
    ) calc
    on tb.id = calc.id

set
	tb.p_home_score = calc.calc_p_home_score,
    tb.p_away_score = calc.calc_p_away_score,
    tb.p_sum_goals = calc.calc_p_sum_goals,
    tb.p_result = calc.calc_p_result,
    tb.p_extra_bet = calc.calc_p_extra_bet,
    tb.p_joker = calc.calc_p_joker,
    tb.total = calc.calc_p_total,
	tb.status = 2

;


set @p_answer = (select value from typerek_conf where name = 'p_answer');

update typerek_answers ta
inner join

    (
    select
    q.status as qstat,          -- question status
    a.status,                   -- answer status
    a.id,                       -- answer ID
    a.question_id_id,           -- answer question
    a.user_id,                  -- answer user ID
    q.answer as qa,             -- correct answer
    a.answer as aa,             -- answer by user

    CASE
        when q.answer = a.answer then @p_answer else 0
    END as 'calc_p_answer'

    from typerek_questions q
    inner join typerek_answers a on q.id = a.question_id_id and q.status = 1 and a.status = 1
    ) calc
    on ta.id = calc.id

set
    ta.p_answer = calc.calc_p_answer,
    ta.status = 2

;





"""

run_sql_statement(sql_statement)