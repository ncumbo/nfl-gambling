import pandas as pd
import numpy as np
from nba_api.stats.static import players, teams
from nba_api.stats import endpoints
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import tkinter as tk

def input_data():
    # window = tk.Tk()
    # window.title("Prop Bet Simulator")
    #
    # l1 = Label(window, text="Teamname:")
    #
    # l1.grid(column=0,row=0)

    # tk.Label(window, text="Teamname:").grid(row=0)
    # tk.Label(window, text="Player Name:").grid(row=1)
    # tk.Label(window, text="Prop Total:").grid(row=2)
    # tk.Label(window, text="Over ML:").grid(row=3)
    # tk.Label(window, text="Under ML:").grid(row=4)
    #
    # teamname = tk.Entry(window)
    # playername = tk.Entry(window)
    # propTotal = tk.Entry(window)
    # overML = tk.Entry(window)
    # underML = tk.Entry(window)
    #
    # teamname.grid(row=0, column=1)
    # playername.grid(row=1, column=1)
    # propTotal.grid(row=2, column=1)
    # overML.grid(row=3, column=1)
    # underML.grid(row=4, column=1)
    # player = np.array([teamname.get(), playername.get(), "Points",propTotal.get(), overML.get(), 0, 0])
    #
    # tk.Button(window, text="Exit", command=window.quit).grid(row=5, column=0, padx=4,pady=4)
    # tk.Button(window, text="Analyze", command=margin(player)).grid(row=5, column=1, padx=4, pady=4)
    #
    # window.mainloop()

    player = np.array(["Jazz","Jordan Clarkson","Points", 16.5, "-113", "-113", 0, 0])
    #check to see if player prop is acceptable and within the margins
    x = margin(player)

def margin(player):
    criteria = {'+110':5,'+100': 4,'-100':3.5, '-105':3.25, '-110': 3, '-115':2.5,'-120': 2,'-125':1.5 ,'-130': 1,'-135':0.75,'-140': 0.5}  # Subject to change depending on ML implementation
    playerID = players.find_players_by_full_name(player[1])[0]['id']      #find player reference number in static
    teamID = endpoints.CommonPlayerInfo(playerID).get_normalized_dict()['CommonPlayerInfo'][0]['TEAM_ID']

    game = endpoints.PlayerNextNGames(player_id=playerID).get_normalized_dict()['NextNGames'][0]
    if game['HOME_TEAM_ID'] == teamID:
        opponentID = game['VISITOR_TEAM_ID']
        #print(game['VISITOR_TEAM_NAME'], game)
    else:
        opponentID = game['HOME_TEAM_ID']
        #print(game['HOME_TEAM_NAME'], game)

    #print(endpoints.Scoreboard().get_normalized_dict())
    #print(endpoints.TeamDashboardByClutch(team_id=teamID, opponent_team_id=opponentID).get_normalized_dict()['OverallTeamDashboard'])
    #print(endpoints.TeamDashboardByTeamPerformance(team_id=teamID, opponent_team_id=opponentID).get_normalized_dict()['PontsAgainstTeamDashboard'])

    #Only accounting for ppg. change variable type in each
    last5 = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last5PlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last5PlayerDashboard'][0]['GP']
    last10 = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last10PlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last10PlayerDashboard'][0]['GP']               #last 10 games (playerdashboardbylastngames)
    regSeasonAve = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['OverallPlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['OverallPlayerDashboard'][0]['GP']       #regular season average (playerdashboardbylastngames)
    try:
        aveAgainstTeam = \
        endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()[
            'OverallPlayerDashboard'][0]['PTS'] / \
        endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()[
            'OverallPlayerDashboard'][0]['GP']  # prop_type average against opposing team (playerdashboardbyopponent)

        #player[6] = (last5*.3 + last10*0.1 + regSeasonAve*.3 + aveAgainstTeam*.3)
        player[6] = (last5 + last10 + regSeasonAve + aveAgainstTeam)/ 4
        print("last 5: ", last5, " last 10: ", last10, " Reg Season: ", regSeasonAve, " Against Team: ", aveAgainstTeam,'\n')

    except:
        player[6] = (last5 + last10 + regSeasonAve) / 3
        print("last 5: ", last5, " last 10: ", last10, " Reg Season: ", regSeasonAve)

    #playoff_ave = 0     #if applicable (PlayerCareerStats['CareerTotalsPostSeason'])

    #

    player[7] = abs(float(player[6]) - float(player[3]))  # + = over margin, - = under margin

    #for both over & under
    #if player[4] and player[5] in criteria:
    if float(player[3]) < float(player[6]):   #If an over
        player = np.append(player, ['over'])
        if 0 <= float(player[7]) <= .5:
            player = np.append(player, ['Confidence: 0 (0 - .5)'])
        elif .5 <= float(player[7]) <= 1:
            if -140 <= float(player[4]) <= -130:
                player = np.append(player, ['Confidence: 1 (.5 - 1)'])
            elif -130 <= float(player[4]):
                player = np.append(player, ['Confidence: 2 (1 - 2.5)'])
            else:
                player = np.append(player, ['Confidence: 0 (0 - .5)'])
        elif 1 <= float(player[7]) <= 2.5:
            if -130 <= float(player[4]) <= -115:
                player = np.append(player, ['Confidence: 2 (1 - 2.5)'])
            elif -115 <= float(player[4]):
                player = np.append(player, ['Confidence: 3 (2.5+)'])
            else:
                player = np.append(player, ['Confidence: 1 (.5 - 1)'])
        elif 2.5 <= float(player[7]):
            if -115 <= float(player[4]):
                player = np.append(player, ['Confidence: 2 (1 - 2.5)'])
            else:
                player = np.append(player, ['Confidence: 3 (2.5+)'])
    else:
        player = np.append(player, ['under'])
        if 0 <= float(player[7]) <= .5:
            player = np.append(player, ['Confidence: 0 (0 - .5)'])
        elif .5 <= float(player[7]) <= 1:
            if -140 <= float(player[5]) <= -130:
                player = np.append(player, ['Confidence: 1 (.5 - 1)'])
            elif -130 <= float(player[5]):
                player = np.append(player, ['Confidence: 2 (1 - 2.5)'])
            else:
                player = np.append(player, ['Confidence: 0 (0 - .5)'])
        elif 1 <= float(player[7]) <= 2.5:
            if -130 <= float(player[5]) <= -115:
                player = np.append(player, ['Confidence: 2 (1 - 2.5)'])
            elif -115 <= float(player[5]):
                player = np.append(player, ['Confidence: 3 (2.5+)'])
            else:
                player = np.append(player, ['Confidence: 1 (.5 - 1)'])
        elif 2.5 <= float(player[7]):
            if -115 <= float(player[5]):
                player = np.append(player, ['Confidence: 2 (1 - 2.5)'])
            else:
                player = np.append(player, ['Confidence: 3 (2.5+)'])

    print(player)
    return 0

def main():
    #Until I click exit button, imput things and then get outputted data
    input_data()

    return

def data_scraper():
    # [Team, Player, Prop, Prop_Total, Over_ML, Under_ML]
    # https://rotogrinders.com/
    #https://www.sportsinteraction.com/basketball/nba-prop-betting/
    # page = requests.get("", {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})
    #page = requests.get("https://betthefarm.club/sports.html?v=1595892817131#!", {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})

    #content = BeautifulSoup(page.content, 'html.parser')
    #print(content)
    # counter = 0
    # for link in content.find_all(class_="row m-0 sportsbook-lines mb-2 border lines_main_container"):
    #     print(link)
    #
    # bet_title = content.find_all(class_="col-12 py-1 border-bottom")
    # bet_line = content.find_all(class_="col-2 p-0 total-lines")
    #
    #
    # print(content, '\n')
    # print(bet_title, '\n')
    # print(bet_line)

    # create player prop


    return 0

if __name__ == "__main__":
    main()