from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import pandas as pd
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(host='localhost',
                               user='ncumbo',
                               password='xT3_N6aR#9$', database="sports_schema")
mycurser = mydb.cursor()    #communicates with mysql database

def data_scrape(date):
    #home team abr; special cases: lar = ram; bal = rav; indy = clt; ari = crd; gb = gnb; hou = htx; ten = oti
    link = "https://www.pro-football-reference.com/boxscores/202009200phi.htm"
    gamblelink = "https://www.vegasinsider.com/nfl/odds/las-vegas/line-movement/rams-@-eagles.cfm/date/09-20-20"
    driver = webdriver.Firefox()
    driver.get(link)
    page = BeautifulSoup(driver.page_source, 'html.parser')

    #date
    game_data = [["Date", "H/A"], ["09/20/2020", "A"], ["09/20/2020", "H"]]

    #Scoreboard
    scoreboard_meta = str(page.find_all("div", class_="scorebox_meta")[0]).split("<div>")
    game_data[0].append("Gametime")
    game_data[1].append(scoreboard_meta[2].split(" ")[2].split("</div>")[0])
    game_data[2].append(scoreboard_meta[2].split(" ")[2].split("</div>")[0])

    #Teamnames
    game_data[0].append("Team")
    game_data[1].append(str(page.find_all("div", class_="box")[0]).split("h1")[1].split(" ")[0][1:] + " " + str(page.find_all("div", class_="box")[0]).split("h1")[1].split(" ")[1])
    game_data[2].append(str(page.find_all("div", class_="box")[0]).split("h1")[1].split(" at ")[1].split("Box Score")[0].split(' - ')[0])

    #Game Info Metadata
    game_info = str(page.find(id="div_game_info")).split("<td class=\"center\" data-stat=\"stat\">")
    game_info.pop(0)
    game_info_clean = []

    for each in range(len(game_info) - 1):
        game_info_clean.append(game_info[each].split("</td>")[0])

    print(game_info_clean)

    game_data[0].append("Won Toss")
    game_data[1].append(game_info_clean[0])
    game_data[2].append(game_info_clean[0])


    #If OT,
    if game_info[0].split("scope=\"row\">")[1].split("</th>")[0] == "Won OT Toss":
        game_data[0].append("Roof")
        game_data[1].append(game_info_clean[2])
        game_data[2].append(game_info_clean[2])
        game_data[0].append("Field Surface")
        game_data[1].append(game_info_clean[3])
        game_data[2].append(game_info_clean[3])
        game_data[0].append("Duration")
        game_data[1].append(game_info_clean[4])
        game_data[2].append(game_info_clean[4])
    else:
        game_data[0].append("Roof")
        game_data[1].append(game_info_clean[1])
        game_data[2].append(game_info_clean[1])
        game_data[0].append("Field Surface")
        game_data[1].append(game_info_clean[2])
        game_data[2].append(game_info_clean[2])
        game_data[0].append("Duration")
        game_data[1].append(game_info_clean[3])
        game_data[2].append(game_info_clean[3])

    #If Dome, set default
    if game_info_clean[1] == "outdoors":
        if 'attendance' not in game_info_clean[4]:      #No fans
            if 'wind' not in game_info_clean[4]:        #No Wind
                game_data[0].append("Weather Tempature")
                game_data[0].append("Wind Speed")
                game_data[1].append("-")
                game_data[2].append("-")
                game_data[1].append("-")
                game_data[2].append("-")
            else:
                game_data[0].append("Weather Tempature")
                game_data[1].append(game_info_clean[4].split(" degrees")[0])
                game_data[1].append(game_info_clean[4].split("wind ")[1])
                game_data[0].append("Wind Speed")
                game_data[2].append(game_info_clean[4].split(" degrees")[0])
                game_data[2].append(game_info_clean[4].split("wind ")[1])
        else:                       #Fans
            game_data[0].append("Weather Tempature")
            game_data[1].append(game_info_clean[5].split(" degrees")[0])
            game_data[1].append(game_info_clean[5].split("wind ")[1])
            game_data[0].append("Wind Speed")
            game_data[2].append(game_info_clean[5].split(" degrees")[0])
            game_data[2].append(game_info_clean[5].split("wind ")[1])
    else:
        game_data[0].append("Weather Tempature")
        game_data[1].append("72")
        game_data[2].append("72")
        game_data[0].append("Wind Speed")
        game_data[1].append("0 mph")
        game_data[2].append("0 mph")

    #Officials
    officials = str(page.find(id="div_officials")).split("<td class=\"center\" data-stat=\"name\">")
    officials.pop(0)

    for each in range(len(officials)):
        officials[each] = officials[each].split(".htm\">")[1].split("</a>")[0]

    print(officials)

    game_data[0].append("Referee")
    game_data[0].append("Umpire")
    game_data[0].append("Down Judge")
    game_data[0].append("Line Judge")
    game_data[0].append("Back Judge")
    game_data[0].append("Side Judge")
    game_data[0].append("Field Judge")

    game_data[1].append(officials[0])
    game_data[1].append(officials[1])
    game_data[1].append(officials[2])
    game_data[1].append(officials[3])
    game_data[1].append(officials[4])
    game_data[1].append(officials[5])
    game_data[1].append(officials[6])
    game_data[2].append(officials[0])
    game_data[2].append(officials[1])
    game_data[2].append(officials[2])
    game_data[2].append(officials[3])
    game_data[2].append(officials[4])
    game_data[2].append(officials[5])
    game_data[2].append(officials[6])

    #Starting QB
    starting_qb = str(page.find(id="player_offense")).split("thead")
    starting_qb.pop(0)
    game_data[0].append("Starting QB")
    game_data[1].append(starting_qb[1].split(".htm\">")[1].split("</a>")[0])
    game_data[2].append(starting_qb[3].split(".htm\">")[1].split("</a>")[0])

    #Score
    scoreboard = str(page.find_all("table", class_="linescore nohover stats_table no_freeze")[0]).split("tbody")[1].split("<tr>")
    a_score = scoreboard[1].split("<td class=\"center\">")
    h_score = scoreboard[2].split("<td class=\"center\">")
    h_score.pop(0)
    h_score.pop(0)
    a_score.pop(0)
    a_score.pop(0)
    for quarter in range(len(h_score) - 1):
        if quarter == 4:
            game_data[0].append("OT")
            game_data[1].append(a_score[quarter].split("</td>")[0])
            game_data[2].append(h_score[quarter].split("</td>")[0])
            break

        game_data[0].append(str(quarter + 1))
        game_data[1].append(a_score[quarter].split("</td>")[0])
        game_data[2].append(h_score[quarter].split("</td>")[0])

    if game_data[0][len(game_data[0]) - 1] != "OT":
        game_data[0].append("OT")
        game_data[1].append(0)
        game_data[2].append(0)

    game_data[0].append("FINAL")
    game_data[1].append(a_score[len(a_score) - 1].split("</td>")[0])
    game_data[2].append(h_score[len(h_score) - 1].split("</td>")[0])

    #Team Stats
    team_stats = str(page.find(id="team_stats")).split("thead")

    game_data[0].append("TEAM ABR")
    game_data[1].append(team_stats[1].split("vis_stat\" scope=\"col\">")[1].split("</th>")[0])
    game_data[2].append(team_stats[1].split("home_stat\" scope=\"col\">")[1].split("</th>")[0])

    vis_team_stats = team_stats[2].split("data-stat=\"vis_stat\">")
    home_team_stats = team_stats[2].split("data-stat=\"home_stat\">")
    vis_team_stats.pop(0)
    home_team_stats.pop(0)

    game_data[0].append("Total First Downs")
    game_data[1].append(vis_team_stats[0].split("</td>")[0])
    game_data[2].append(home_team_stats[0].split("</td>")[0])
    game_data[0].append("Rush Atts")
    game_data[1].append(vis_team_stats[1].split("-")[0])
    game_data[2].append(home_team_stats[1].split("-")[0])
    game_data[0].append("Rush Yrds")
    game_data[1].append(vis_team_stats[1].split("-")[1])
    game_data[2].append(home_team_stats[1].split("-")[1])
    game_data[0].append("Rush TDs")
    game_data[1].append(vis_team_stats[1].split("-")[2].split("</td>")[0])
    game_data[2].append(home_team_stats[1].split("-")[2].split("</td>")[0])
    game_data[0].append("Pass Cmps")
    game_data[1].append(vis_team_stats[2].split("-")[0])
    game_data[2].append(home_team_stats[2].split("-")[0])
    game_data[0].append("Pass Atts")
    game_data[1].append(vis_team_stats[2].split("-")[1])
    game_data[2].append(home_team_stats[2].split("-")[1])
    game_data[0].append("Pass Yrds")
    game_data[1].append(vis_team_stats[2].split("-")[2])
    game_data[2].append(home_team_stats[2].split("-")[2])
    game_data[0].append("Passing TDs")
    game_data[1].append(vis_team_stats[2].split("-")[3])
    game_data[2].append(home_team_stats[2].split("-")[3])
    game_data[0].append("Interceptions")
    game_data[1].append(vis_team_stats[2].split("-")[4].split("</td>")[0])
    game_data[2].append(home_team_stats[2].split("-")[4].split("</td>")[0])
    game_data[0].append("Sacks Taken")
    game_data[1].append(vis_team_stats[3].split("-")[0])
    game_data[2].append(home_team_stats[3].split("-")[0])
    game_data[0].append("Sacks Taken Yrds")
    game_data[1].append(vis_team_stats[3].split("-")[1].split("</td>")[0])
    game_data[2].append(home_team_stats[3].split("-")[1].split("</td>")[0])
    game_data[0].append("Total Yards")
    game_data[1].append(vis_team_stats[5].split("</td>")[0])
    game_data[2].append(home_team_stats[5].split("</td>")[0])
    game_data[0].append("Fumbles")
    game_data[1].append(vis_team_stats[6].split("-")[0])
    game_data[2].append(home_team_stats[6].split("-")[0])
    game_data[0].append("Fumbles Lost")
    game_data[1].append(vis_team_stats[6].split("-")[1].split("</td>")[0])
    game_data[2].append(home_team_stats[6].split("-")[1].split("</td>")[0])
    game_data[0].append("Turnovers")
    game_data[1].append(vis_team_stats[7].split("</td>")[0])
    game_data[2].append(home_team_stats[7].split("</td>")[0])
    game_data[0].append("Penalties")
    game_data[1].append(vis_team_stats[8].split("-")[0])
    game_data[2].append(home_team_stats[8].split("-")[0])
    game_data[0].append("Penalty Yrds")
    game_data[1].append(vis_team_stats[8].split("-")[1].split("</td>")[0])
    game_data[2].append(home_team_stats[8].split("-")[1].split("</td>")[0])
    game_data[0].append("3rd Down Completed")
    game_data[1].append(vis_team_stats[9].split("-")[0])
    game_data[2].append(home_team_stats[9].split("-")[0])
    game_data[0].append("3rd Down Attempts")
    game_data[1].append(vis_team_stats[9].split("-")[1].split("</td>")[0])
    game_data[2].append(home_team_stats[9].split("-")[1].split("</td>")[0])
    game_data[0].append("4th Down Completed")
    game_data[1].append(vis_team_stats[10].split("-")[0])
    game_data[2].append(home_team_stats[10].split("-")[0])
    game_data[0].append("4th Down Attempts")
    game_data[1].append(vis_team_stats[10].split("-")[1].split("</td>")[0])
    game_data[2].append(home_team_stats[10].split("-")[1].split("</td>")[0])
    game_data[0].append("Time of Possession")
    game_data[1].append(vis_team_stats[11].split("</td>")[0])
    game_data[2].append(home_team_stats[11].split("</td>")[0])

    #footballdb.com data

    #vegasinsider.com data
    driver = webdriver.Firefox()
    driver.get(gamblelink)
    page = BeautifulSoup(driver.page_source, 'html.parser')

    odds_table = str(page.find_all("table", class_="rt_railbox_border2")[1]).split("<tr>")
    odds_table.pop(0)
    x = 0
    for row in range(len(odds_table) - 1):
        row_data = odds_table[row].split("nowrap=\"\">")
        row_data.pop(0)
        if len(row_data) == 10:
            x = row
            break

    #Get Opening Odds - odds_table[x]
    opening_odds = odds_table[x].split("nowrap=\"\">")
    opening_odds.pop(0)
    opening_odds.pop(0)
    opening_odds.pop(0)

    #Get Closing Odds - odds_table[len(odds_table) - 1]
    closing_odds = odds_table[len(odds_table) - 1].split("nowrap=\"\">")
    closing_odds.pop(0)
    closing_odds.pop(0)
    closing_odds.pop(0)

    for dp in range(len(opening_odds)):
        if "b20000" in opening_odds[dp]:
            opening_odds[dp] = str(str(opening_odds[dp].split()[1]).split(">")[1]).split("<")[0] + str(str(opening_odds[dp].split()[2]).split(">")[1]).split("<")[0]
        else:
            opening_odds[dp] = opening_odds[dp].split()[0] + opening_odds[dp].split()[1].split("</td>")[0]        #opening_odds[dp] = opening_odds[dp].split()[0].split("</td>")[0]


    for dp in range(len(closing_odds)):
        if "b20000" in closing_odds[dp]:
            if len(closing_odds[dp].split()) == 1:
                closing_odds[dp] = closing_odds[dp].split()[0]
            else:
                closing_odds[dp] = str(closing_odds[dp].split()[0].split("<")[0]) + str((str(closing_odds[dp].split()[1]) + str(closing_odds[dp].split()[2])).split("\"b20000\">")[1].split("</font>")[0])
        else:
            closing_odds[dp] = closing_odds[dp].split()[0] + closing_odds[dp].split()[1].split("</td>")[0]

        #which team goes where
    print(opening_odds)
    print(closing_odds)

    print(game_data[1][24], opening_odds[0][:3], opening_odds[3][3:-4])

    game_data[0].append("ML Open")  #opening_odds
    if game_data[1][24] == opening_odds[0][:3]:                                #SWITCH 2 to 24
        game_data[1].append(opening_odds[0][-4:])
        game_data[2].append(opening_odds[1][-4:])
    else:
        game_data[1].append(opening_odds[1][-4:])
        game_data[2].append(opening_odds[0][-4:])
    game_data[0].append("ML Close") #closing_odds
    if game_data[1][24] == closing_odds[0].split("-")[0]:                                #SWITCH 2 to 24
        game_data[1].append(closing_odds[0][-4:])
        game_data[2].append(closing_odds[1][-4:])
    else:
        game_data[1].append(closing_odds[1][-4:])
        game_data[2].append(closing_odds[0][-4:])

    game_data[0].append("Spread Open")  #opening_odds
    if game_data[1][24] == opening_odds[2][:3]:                                #SWITCH 2 to 24
        game_data[1].append(opening_odds[2][3:-4])
        game_data[2].append(opening_odds[3][3:-4])

    else:  # Team 2 is Favorite
        game_data[1].append(opening_odds[3][3:-4])
        game_data[2].append(opening_odds[2][3:-4])

    game_data[0].append("Spread Odds Open") #opening_odds
    if game_data[1][24] == opening_odds[2][:3]:                                #SWITCH 2 to 24
        game_data[2].append(opening_odds[3][-4:])
        game_data[1].append(opening_odds[2][-4:])

    else:  # Team 2 is Favorite
        game_data[2].append(opening_odds[2][-4:])
        game_data[1].append(opening_odds[3][-4:])

    game_data[0].append("Spread Close") #closing_odds
    if game_data[1][24] == closing_odds[2][:3]:                                #SWITCH 2 to 24
        game_data[1].append(closing_odds[2][3:-4])
        game_data[2].append(closing_odds[3][3:-4])

    else:  # Team 2 is Favorite
        game_data[1].append(closing_odds[3][3:-4])
        game_data[2].append(closing_odds[2][3:-4])

    game_data[0].append("Spread Close Odds")    #closing_odds
    if game_data[1][24] == closing_odds[2][:3]:                                  #SWITCH 2 to 24
        game_data[2].append(closing_odds[3][-4:])
        game_data[1].append(closing_odds[2][-4:])


    else:  # Team 2 is Favorite
        game_data[2].append(closing_odds[2][-4:])
        game_data[1].append(closing_odds[3][-4:])

    game_data[0].append("O/U Open") #opening_odds
    if "-" in opening_odds[4]:
        game_data[1].append(opening_odds[4].split("-")[0])
        game_data[2].append(opening_odds[5].split("-")[0])
    else:
        game_data[1].append(opening_odds[4].split("+")[0])
        game_data[2].append(opening_odds[5].split("+")[0])
    game_data[0].append("O/U Open Odds")    #opening_odds
    game_data[1].append(opening_odds[4][-4:])
    game_data[2].append(opening_odds[5][-4:])

    game_data[0].append("O/U Close")    #closing_odds
    if "-" in closing_odds[4]:
        game_data[1].append(closing_odds[4].split("-")[0])
        game_data[2].append(closing_odds[5].split("-")[0])
    else:
        game_data[1].append(closing_odds[4].split("+")[0])
        game_data[2].append(closing_odds[5].split("+")[0])
    game_data[0].append("O/U Close Odds")   #closing_odds
    game_data[1].append(closing_odds[4][-4:])
    game_data[2].append(closing_odds[5][-4:])


    game_data[0].append("1H Spread Open")   #opening_odds
    if game_data[1][24] == str(opening_odds[6][:3]):                                   #SWITCH 2 to 24
        if str(closing_odds[6][-2:]) == "PK":
            game_data[1].append("PK")
            game_data[2].append("PK")
        else:
            game_data[1].append("-" + opening_odds[6].split("-")[1])
            game_data[2].append("+" + opening_odds[7].split("+")[1])
    else:                                                   #Team 2 is Fav
        if str(closing_odds[7][-2:]) == "PK":
            game_data[1].append("PK")
            game_data[2].append("PK")
        else:
            game_data[1].append("+" + opening_odds[7].split("+")[1])
            game_data[2].append("-" + opening_odds[6].split("-")[1])
    game_data[0].append("1H Spread Open Odds")  #opening_odds
    game_data[1].append("-110")
    game_data[2].append("-110")
    game_data[0].append("1H Spread Close")  #closing_odds
    if game_data[1][24] == str(closing_odds[6][:3]):                                #SWITCH 2 to 24
        if str(closing_odds[6][-2:]) == "PK":
            game_data[1].append("PK")
            game_data[2].append("PK")
        else:
            game_data[1].append("-" + closing_odds[6].split("-")[1])
            game_data[2].append("+" + closing_odds[7].split("+")[1])
    else:                                                   #Team 2 is Fav
        if str(closing_odds[7][-2:]) == "PK":
            game_data[1].append("PK")
            game_data[2].append("PK")
        else:
            game_data[1].append("+" + closing_odds[7].split("+")[1])
            game_data[2].append("-" + closing_odds[6].split("-")[1])
    game_data[0].append("1H Spread Close Odds") #closing_odds
    game_data[1].append("-110")
    game_data[2].append("-110")


    print(game_data[0])
    print(game_data[1])
    print(game_data[2])

    print(game_data[1][60])



    # Save Data to Database
    sql = "INSERT INTO nfl_db_2020" \
          "(date_, h_a, gametime, team, won_toss, roof, field_surface, duration, weather, wind_speed, head_referee, umpire, down_judge, line_judge, back_judge, side_judge, field_judge, starting_qb,"\
          " q1, q2, q3, q4, ot, final_score, team_abr, first_downs, rush_att, rush_yrds, rush_tds, pass_cmps, pass_att, pass_yrds, pass_tds, pass_ints, sacks_taken, sacks_taken_yrds,"\
          " total_yrds, fumbles, tot_fumbles_lost, turnovers, penalties, penalty_yrds, 3rd_down_comp, 3rd_down_att, 4th_down_comp, 4th_down_att, time_of_poss, ml_open, ml_close, "\
          "spread_open, spread_open_odds, spread_close, spread_close_odds, ou_open, ou_open_odds, ou_close, ou_close_odds, 1h_spread_open, 1h_spread_open_odds, 1h_spread_close, 1h_spread_close_odds)"\
          " Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "\
          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (game_data[1][0], game_data[1][1], game_data[1][2], game_data[1][3], game_data[1][4], game_data[1][5], game_data[1][6], game_data[1][7], game_data[1][8], game_data[1][9], game_data[1][10], game_data[1][11], game_data[1][12], game_data[1][13], game_data[1][14], game_data[1][15], game_data[1][16], game_data[1][17], game_data[1][18], game_data[1][19], game_data[1][20], game_data[1][21], game_data[1][22], game_data[1][23], game_data[1][24], game_data[1][25], game_data[1][26], game_data[1][27], game_data[1][28], game_data[1][29], game_data[1][30], game_data[1][31], game_data[1][32], game_data[1][33], game_data[1][34], game_data[1][35], game_data[1][36], game_data[1][37], game_data[1][38], game_data[1][39], game_data[1][40], game_data[1][41], game_data[1][42], game_data[1][43], game_data[1][44], game_data[1][45], game_data[1][46], game_data[1][47], game_data[1][48], game_data[1][49], game_data[1][50], game_data[1][51], game_data[1][52], game_data[1][53], game_data[1][54], game_data[1][55], game_data[1][56], game_data[1][57], game_data[1][58], game_data[1][59], game_data[1][60])
    mycurser.execute(sql, val)
    mydb.commit()

    sql = "INSERT INTO nfl_db_2020" \
          "(date_, h_a, gametime, team, won_toss, roof, field_surface, duration, weather, wind_speed, head_referee, umpire, down_judge, line_judge, back_judge, side_judge, field_judge, starting_qb,"\
          " q1, q2, q3, q4, ot, final_score, team_abr, first_downs, rush_att, rush_yrds, rush_tds, pass_cmps, pass_att, pass_yrds, pass_tds, pass_ints, sacks_taken, sacks_taken_yrds,"\
          " total_yrds, fumbles, tot_fumbles_lost, turnovers, penalties, penalty_yrds, 3rd_down_comp, 3rd_down_att, 4th_down_comp, 4th_down_att, time_of_poss, ml_open, ml_close, "\
          "spread_open, spread_open_odds, spread_close, spread_close_odds, ou_open, ou_open_odds, ou_close, ou_close_odds, 1h_spread_open, 1h_spread_open_odds, 1h_spread_close, 1h_spread_close_odds)"\
          " Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "\
          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (game_data[2][0], game_data[2][1], game_data[2][2], game_data[2][3], game_data[2][4], game_data[2][5], game_data[2][6], game_data[2][7], game_data[2][8], game_data[2][9], game_data[2][10], game_data[2][11], game_data[2][12], game_data[2][13], game_data[2][14], game_data[2][15], game_data[2][16], game_data[2][17], game_data[2][18], game_data[2][19], game_data[2][20], game_data[2][21], game_data[2][22], game_data[2][23], game_data[2][24], game_data[2][25], game_data[2][26], game_data[2][27], game_data[2][28], game_data[2][29], game_data[2][30], game_data[2][31], game_data[2][32], game_data[2][33], game_data[2][34], game_data[2][35], game_data[2][36], game_data[2][37], game_data[2][38], game_data[2][39], game_data[2][40], game_data[2][41], game_data[2][42], game_data[2][43], game_data[2][44], game_data[2][45], game_data[2][46], game_data[2][47], game_data[2][48], game_data[2][49], game_data[2][50], game_data[2][51], game_data[2][52], game_data[2][53], game_data[2][54], game_data[2][55], game_data[2][56], game_data[2][57], game_data[2][58], game_data[2][59], game_data[2][60])
    mycurser.execute(sql, val)
    mydb.commit()

def main():
    date = "09/08/2019" #input("Enter date as mm/dd/yyyy: ")
    data_scrape(date)
    #each team rankings after each week

    return

if __name__ == "__main__":
    main()
