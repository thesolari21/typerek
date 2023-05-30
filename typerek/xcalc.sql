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
	b.status,
	b.id,
	b.match_id_id,
	b.user_id,
	m.multiplier,
	m.team_home_score as mths,
	m.team_away_score as mtas,
	m.extra_bet_result,
	b.team_home_score as bths,
	b.team_away_score as btas,
	b.extra_bet,
	b.joker,

	CASE
		when m.team_home_score = b.team_home_score then @p_home_score
		else 0
	END as 'calc_p_home_score',
	CASE
		when m.team_away_score = b.team_away_score then @p_away_score
		else 0
	END as 'calc_p_away_score',
	CASE
		when (m.team_away_score + m.team_home_score)  = (b.team_away_score + b.team_home_score) then @p_sum_goals
		else 0
	END as 'calc_p_sum_goals',
	CASE
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) * (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) > 0 then @p_result
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) = (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) then @p_result
		else 0
	END as 'calc_p_result',
	CASE
		when m.extra_bet_result = b.extra_bet then @p_extra_bet
		else 0
	END as 'calc_p_extra_bet',
	CASE
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) * (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) > 0 then @p_joker * b.joker
		when (CAST(m.team_home_score as signed) - cast(m.team_away_score as signed)) = (cast(b.team_home_score as signed) - cast(b.team_away_score as signed)) then @p_joker * b.joker
		else cast(@p_joker as signed) * cast(b.joker as signed) * -1
	END as 'calc_p_joker'

	from typerek_matches m
	inner join typerek_bets b
	on m.id = b.match_id_id and b.status = 1
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
where
	tb.status = 1
;