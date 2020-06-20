import csv
import mysql.connector
from columns import *
import pandas as pd

mydb = mysql.connector.connect(host='localhost', user='root', password='xT3_N6aR#9$', database="gambledb")
mycurser = mydb.cursor()    #communicates with mysql database

# mycurser.execute("CREATE TABLE ml_week_by_week (teamname VARCHAR(255), ave_1q_score FLOAT (10))")#create table
#
# sqlFormula = "INSERT INTO ml_week_by_week (teamname, ave_1q_score) VALUES (%s, %s)"
# weeks = [
#     (1,0),
#     (2,0),
#     (3,0),
#     (4,0),
#     (5,0),
#     (6,0),
#     (7,0),
#     (8,0),
#     (9,0),
#     (10,0),
#     (11,0),
#     (12,0),
#     (13,0),
#     (14,0),
#     (15,0),
#     (16, 0),
#     (17, 0),
#     (18, 0),
#     (19, 0),
#     (20, 0),
#     (21, 0),
# ]
# teams = [
#     ('Arizona Cardinals', 0,0,0),
#     ('Atlanta Falcons', 0,0,0),
#     ('Baltimore Ravens', 0,0,0),
#     ('Buffalo Bills', 0,0,0),
#     ('Carolina Panthers', 0,0,0),
#     ('Chicago Bears', 0,0,0),
#     ('Cincinnati Bengals', 0,0,0),
#     ('Cleveland Browns', 0,0,0),
#     ('Dallas Cowboys', 0,0,0),
#     ('Denver Broncos', 0,0,0),
#     ('Detroit Lions', 0,0,0),
#     ('Green Bay Packers', 0,0,0),
#     ('Houston Texans', 0,0,0),
#     ('Indianapolis Colts', 0,0,0),
#     ('Jacksonville Jaguars', 0,0,0),
#     ('Kansas City Chiefs', 0,0,0),
#     ('Los Angeles Chargers', 0,0,0),
#     ('Los Angeles Rams', 0,0,0),
#     ('Miami Dolphins', 0,0,0),
#     ('Minnesota Vikings', 0,0,0),
#     ('New England Patriots', 0,0,0),
#     ('New Orleans Saints', 0,0,0),
#     ('New York Giants', 0,0,0),
#     ('New York Jets', 0,0,0),
#     ('Oakland Raiders', 0,0,0),
#     ('Philadelphia Eagles', 0,0,0),
#     ('Pittsburgh Steelers', 0,0,0),
#     ('San Francisco 49ers', 0,0,0),
#     ('Seattle Seahawks', 0,0,0),
#     ('Tampa Bay Buccaneers', 0,0,0),
#     ('Tennessee Titans', 0,0,0),
#     ('Washington Redskins', 0,0,0),
# ]

#mycurser.executemany(sqlFormula,weeks)
# mycurser.execute("ALTER TABLE ml_week_by_week MODIFY COLUMN ave_1q_score FLOAT")

x=0
#mycurser.execute("ALTER TABLE ml_week_by_week DROP COLUMN ave_penalty_yrds")
# mycurser.execute("ALTER TABLE ml_week_by_week ADD ml_score_q4_dog FLOAT(10) after ml_score_q4_fav")
# mycurser.execute("UPDATE ml_week_by_week SET ml_score_q4_dog = 0")
# mydb.commit()

#62 columns
def main():
    team_arr = []

    mycurser.execute("SELECT * FROM ml_week_by_week")
    result = mycurser.fetchall()
    for row in result:
        team_arr.append(list(row))  #double list

    data = pd.read_csv("NO-TITLE-2019-NFL-Stats.csv")

    # with open('NO-TITLE-2019-NFL-Stats.csv', newline='') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',')
    #     for column in reader:  #Reads each column. Start by reading 2nd line
    #         columns(column)
    #        for week in team_arr:
    #             if week[0] == game_week:
    #                 x=1
    #                 #weekly_leading_at_quarters(week, column, ml, team_score, opponent_score, q1, q2, q3, team_arr)
    #
    #                 if int(ml) < 0:  #negative/favorite
    #                     money_won = round(100 * (100/abs(int(ml))), 2)
    #                     money_lost = -100
    #                     if int(team_score) > int(opponent_score):
    #                         week[28] += money_won
    #                     else:
    #                         week[28] += money_lost
    #
    #                 else:       #positive/dog
    #                     money_won = round(100 * (int(ml)/100), 2)
    #                     money_lost = -100
    #                     if int(team_score) > int(opponent_score):
    #                         week[29] += money_won
    #                     else:
    #                         week[29] += money_lost
    #
    #                 week[28] = round(week[28], 2)
    #                 week[29] = round(week[29], 2)
    #
    # print(type(team_arr))
    # for each in team_arr:
    #     #each[25] = round(each[25] / each[1],1)
    #     # sql = "UPDATE ml_week_by_week SET ml_fav_profit = %s, ml_dog_profit = %s WHERE teamname = %s"
    #     # input = (each[28], each[29],  each[0])
    #     # mycurser.execute(sql, input)
    #     # mydb.commit()
    #     print(each)



    return 0

def read_game_by_game(team_arr):
    with open("2019-NFL-Stats.csv", 'r') as file:

        matchup = []

        for i in range(2):  #read 2 files
            matchup.append(file.readline())
            #do something

    # leading @ q1 (fav,dogs) (30,31)
    # ML (fav,dogs) (32,33)

    # leading @ HT   (fav,dogs) (34,35)
    # ML (fav,dogs) (36,37)
    # scoring more in q2 (fav,dogs) (38,39)
    # ML (fav,dogs) (40,41)

    # leading @ Q3   (fav,dogs) (42,43)
    # ML (fav,dogs) (44,45)
    # scoring more in q3 (fav,dogs) (46,47)
    # ML (fav,dogs) (48,49)

    # scoring more in q2 (fav,dogs) (50,51)
    # ML (fav,dogs) (52,53)
    return

# #average team trends
def mov(column, team, team_score, opponent_score):
    if column[3] == str(1):
        team[2] = 0

    team[1] += int(team_score) - int(opponent_score)
    team[2] += 1

    #team[1] = round(team[1] / team[2],1)

def ats(column, team, team_score, opponent_score, spread):  #average points team covers the spread by +-
    if column[3] == str(1):
        team[1] = 0

    diff = int(team_score) - int(opponent_score)
    team[2] += diff + float(spread)
    team[1] += 1

    # each[3] = round(each[2] / each[1], 1)

def average_home_away_score(column, team, home_v_away, team_score):
    if column[3] == str(1):
        team[1] = 0
        team[2] = 0

    if home_v_away == "Home":
        team[4] += int(team_score)
        team[1] += 1
    else:
        team[5] += int(team_score)
        team[2] += 1

    # each[4] = round(each[4] / each[1], 1)
    # each[5] = round(each[5] / each[2], 1)


def average_ou_home_away(column, team, ou, opponent_score, team_score, home_v_away):
    if column[3] == str(1):
        team[1] = 0
        team[2] = 0
        team[3] = 0
        team[4] = 0

    if home_v_away == "Home":
        if float(ou) < int(opponent_score) + int(team_score):   #over
            team[8] += int(team_score)
            team[1] += 1
        else:       #under
            team[10] += int(team_score)
            team[2] += 1
    else:
        if float(ou) < int(opponent_score) + int(team_score):   #over
            team[9] += int(team_score)
            team[3] += 1
        else:       #under
            team[11] += int(team_score)
            team[4] += 1

    # each[8] = round(each[8] / each[1], 1)
    # each[9] = round(each[9] / each[3], 1)
    # each[10] = round(each[10] / each[2], 1)
    # each[11] = round(each[11] / each[4], 1)

def average_score_when_last_game_is_ou(column, team, ou, opponent_score, team_score):
    if column[3] == str(1):
        team[1] = "N"  # prev game over (O, U, N)
        team[2] = 0  # number of games with the previous game going over
        team[4] = 0  # number of games with the previous game going under

        if float(ou) < int(opponent_score) + int(team_score):  # over
            team[1] = "O"
        else:  # under
            team[1] = "U"

    else:
        if team[1] == "O":  # if previous game was over
            team[12] += int(team_score)
            team[2] += 1

        else:  # if previous game was under
            team[13] += int(team_score)
            team[4] += 1

        if float(ou) < int(opponent_score) + int(team_score):  # over
            team[1] = "O"
        else:  # under
            team[1] = "U"

    # each[12] = round(each[12] / each[2], 1)
    # each[13] = round(each[13] / each[4], 1)

def average_spread_when_spread_wl(column, team_score, opponent_score, spread, team):
    if column[3] == str(1):
        team[1] = 0
        team[2] = 0

    diff = int(team_score) - int(opponent_score)
    if diff > -float(spread):
        team[14] += float(spread)
        team[1] += 1

    elif diff < -float(spread):
        team[15] += float(spread)
        team[2] += 1

    # each[14] = round(each[14] / each[1], 1)
    # each[15] = round(each[15] / each[2], 1)

def ave_spread_under_fav(column, team, spread):
    if column[3] == str(1):
        team[1] = 0
        team[2] = 0

    if float(spread) < 0:   #favorite
        team[19] += float(spread)
        team[2] += 1

    else:   #dog
        team[18] += float(spread)
        team[1] += 1


    # if each[18] != 0:
    #     each[18] = round(each[18] / each[1], 1)
    # if each[19] != 0:
    #     each[19] = round(each[19] / each[2], 1)
def ave_spread_fav_und_when_win_loss(column, team, team_score, opponent_score, spread):
    if column[3] == str(1):
        team[1] = 0
        team[2] = 0
        team[3] = 0
        team[4] = 0

    diff = int(team_score) - int(opponent_score)
    if float(spread) < 0:  # favorite
        if diff > -float(spread):  # won
            team[22] += float(spread)
            team[3] += 1

        elif diff < -float(spread):  # loss
            team[23] += float(spread)
            team[4] += 1
    else:  # dog
        if diff > -float(spread):  # won
            team[20] += float(spread)
            team[1] += 1

        elif diff < -float(spread):  # loss
            team[21] += float(spread)
            team[2] += 1
    # if each[20] != 0:
    #     each[20] = round(each[20] / each[1], 1)
    # if each[21] != 0:
    #     each[21] = round(each[21] / each[2], 1)
    # if each[22] != 0:
    #     each[22] = round(each[22] / each[3], 1)
    # if each[23] != 0:
    #     each[23] = round(each[23] / each[4], 1)
def ave_over_under_when_over_under_hits(column, team, team_score, opponent_score, ou):
    if column[3] == str(1):
        team[1] = 0  # 24 average o/u per game
        team[2] = 0  # 25 average o when o hit
        team[3] = 0  # 26 average u when u hit
        team[4] = 0  # 27 average o when team wins
        team[5] = 0  # 28 average o when team losses
        team[6] = 0  # 29 average u when team wins
        team[7] = 0  # 30 average u when team losses

    diff = int(team_score) + int(opponent_score)
    team[24] += float(ou)
    team[1] += 1
    if float(ou) < diff:  # over
        team[25] += diff
        team[2] += 1

        if int(team_score) > int(opponent_score):  # won
            team[27] += diff
            team[4] += 1
        else:  # loss
            team[28] += diff
            team[5] += 1

    else:  # under
        team[26] += diff
        team[3] += 1

        if int(team_score) > int(opponent_score):  # won
            team[29] += diff
            team[6] += 1
        else:  # loss
            team[30] += diff
            team[7] += 1
    # each[24] = round(each[24] / each[1], 1)
    # each[25] = round(each[25] / each[2], 1)
    # each[26] = round(each[26] / each[3], 1)
    # each[27] = round(each[27] / each[4], 1)
    # each[28] = round(each[28] / each[5], 1)
    # each[29] = round(each[29] / each[6], 1)
    # each[30] = round(each[30] / each[7], 1)

#week by week stats
def weekly_trends(week, column, ml, team_score, opponent_score):
    week[2] += float(column[6])
    week[3] += float(column[7])
    week[4] += float(column[6]) + float(column[7])
    week[5] += float(column[8])
    week[6] += float(column[9])
    if column[10] != '':
        week[7] += int(column[10])
    week[8] += float(column[11])
    week[9] += float(column[13])
    week[10] += float(column[14])
    week[11] += float(column[15])
    week[12] += float(column[16])
    week[13] += float(column[17])
    week[14] += float(column[18])
    week[15] += float(column[19])
    week[16] += float(column[20])
    week[17] += float(column[21])
    week[18] += float(column[22])
    week[19] += float(column[24])
    week[20] += float(column[25])
    week[21] += float(column[28])
    week[22] += float(column[29])
    week[23] += float(column[30])
    week[24] += float(column[35])
    week[25] += float(column[36])

    if int(ml) < 0:  # negative/favorite
        money_won = round(100 * (100 / abs(int(ml))), 2)
        money_lost = -100
        if int(team_score) > int(opponent_score):
            week[28] += money_won
        else:
            week[28] += money_lost

    else:  # positive/dog
        money_won = round(100 * (int(ml) / 100), 2)
        money_lost = -100
        if int(team_score) > int(opponent_score):
            week[29] += money_won
        else:
            week[29] += money_lost

    week[28] = round(week[28], 2)
    week[29] = round(week[29], 2)
    return



if __name__ == "__main__":
    main()