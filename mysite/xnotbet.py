import mysql.connector
import os
import environ
import collections
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

env = environ.Env()
environ.Env.read_env()

def send_email_to_player(to_email, player_name, matches):
    """Funkcja wysyła prostego maila w HTML do gracza"""

    try:

        # konfiguracja serwera poczty
        smtp_host = env('EMAIL_HOST')
        smtp_user = env('EMAIL_HOST_USER')
        smtp_pass = env('EMAIL_HOST_PASSWORD')
        subject = f"Twoje nieobstawione mecze"

        # budujemy treść HTML maila
        html_content = f"<h2>Cześć {player_name}!</h2>"
        html_content += "<p>Poniżej lista NIEOBSTAWIONYCH spotkań które niebawem się rozpoczną. Rusz się, bo potem znowu będziesz płakać, że zapomniałeś... </p><ul>"

        for rec in matches:
            html_content += f"<li>{rec['mecz']} | {rec['data']}</li>"

        html_content += "</ul>"
        html_content += "<p>Nie pozdrawiam,<br>Typerek</p>"
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        # wysyłka maila
        with smtplib.SMTP(smtp_host, 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print(f" Wysłano email do: {to_email}")

    except Exception as e:
        print(f" Błąd wysyłki maila do {to_email}: {e}")


def run_sql_statement(sql_statement):
    config = {
        'user': env('DATABASE_USER'),
        'password': env('DATABASE_PASS'),
        'host': env('DATABASE_HOST'),
        'database': env('DATABASE_NAME'),
        'raise_on_warnings': True
    }

    grouped_results = collections.defaultdict(list)

    try:
        with mysql.connector.connect(**config) as connection:
            with connection.cursor(dictionary=True) as cursor:

                cursor.execute(sql_statement)
                rows = cursor.fetchall()

                for row in rows:
                    grouped_results[row["gracz"]].append(row)

                print("=== WYNIKI ===")

                # rozpakowanie krotek (user, [rekordy])

                for user, records in grouped_results.items():
                    print(f"\nGracz: {user}")
                    for rec in records:
                        print(f"  - {rec['mecz']} | {rec['data']} | status={rec['status_typu']} | {rec['email']} ")

                    # po wypisaniu danych wywołujemy wysyłkę maila
                    if records:
                        send_email_to_player(records[0]["email"], user, records)

    except mysql.connector.Error as error:
        print("Błąd wykonania wyrażenia SQL:", error)

    return grouped_results


sql_statement = """

SELECT
    e.username AS gracz,
    e.name AS liga,
    e.id AS id_mecz,
    CONCAT(e.team_home_name,'-',e.team_away_name) AS mecz,
    CONVERT_TZ(e.`date`, '+00:00', 'Europe/Warsaw') AS data,
    CONVERT_TZ(NOW(), '+00:00', 'Europe/Warsaw') AS godzina_systemowa,
    e.tb_id AS id_typu,
    e.tb_status AS status_typu,
    e.email AS email,
    e.nottification_articles AS nott_brak_typu

FROM (
    SELECT
        d.*,
        tb.id AS tb_id,
        tb.status AS tb_status

    FROM (
        SELECT
            b.*,
            c.id,
            c.`date`,
            c.team_home_name,
            c.team_away_name
            
        FROM (
            SELECT
                a.*,
                au.username,
                au.email,
                tu2.nottification_articles,
                tu2.user_id as user_id_ext_profile

            FROM (
                SELECT
                    tu.user_id,
                    tu.league_id,
                    tl.name

                FROM typerek_usersleagues tu
                INNER JOIN typerek_league tl
                  ON tu.league_id = tl.id
                 AND tl.status = 1
            ) a

            INNER JOIN auth_user au
              ON au.id = a.user_id
            INNER JOIN typerek_userprofile tu2
              on tu2.user_id = au.id

        ) b

        INNER JOIN (
            SELECT *
            FROM typerek_matches tm
            WHERE DATE(tm.`date`) = CURDATE()
              AND status = 0

        ) c ON b.league_id = c.league_id

    ) d

    LEFT JOIN typerek_bets tb
      ON d.id = tb.match_id_id
     AND d.user_id = tb.user_id
    WHERE tb.status IS NULL OR tb.status = 0

) AS e

WHERE
e.email <> '' and
e.nottification_articles = 1

ORDER BY e.username;

"""

grouped = run_sql_statement(sql_statement)