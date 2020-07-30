import pandas as pd
import numpy as np
from nba_api.stats.static import players, teams
from nba_api.stats import endpoints
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from dataclasses import dataclass

@dataclass
class player_prop:
    team: str
    player_name: str
    prop_type: str
    prop_total: int
    over_ml: str
    under_ml: str
    player_average: int = 0
    over_or_under: str = ""

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
    acceptable_bets = []
    #player = player_prop("Lakers","Lebron James","Points", 27.5, "-130", "-110")
    player = player_prop("Grizzlies","Ja Morant", "Points", 17, "-120", "-120")
    player = np.array(["Pelicans","Brandon Ingram", "Points", 22.5, "-129", "+100", 0, 0])
    #check to see if player prop is acceptable and within the margins
    x = margin(player)

    return 0

def margin(player):
    criteria = {'+110':5,'+100': 4,'-100':3.5, '-105':3.25, '-110': 3, '-115':2.5,'-120': 2,'-125':1.5 ,'-130': 1,'-135':0.75,'-140': 0.5}  # Subject to change depending on ML implementation
    print(criteria)
    playerID = players.find_players_by_full_name(player[1])[0]['id']      #find player reference number in static
    teamID = endpoints.CommonPlayerInfo(playerID).get_normalized_dict()['CommonPlayerInfo'][0]['TEAM_ID']

    game = endpoints.PlayerNextNGames(player_id=playerID).get_normalized_dict()['NextNGames'][0]
    if game['HOME_TEAM_ID'] == teamID:
        opponentID = game['VISITOR_TEAM_ID']
        #print(game['VISITOR_TEAM_NAME'], game)
    else:
        opponentID = game['HOME_TEAM_ID']
        #print(game['HOME_TEAM_NAME'], game)


    #Only accounting for ppg. change variable type in each
    last5 = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last5PlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last5PlayerDashboard'][0]['GP']
    last10 = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last10PlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last10PlayerDashboard'][0]['GP']               #last 10 games (playerdashboardbylastngames)
    regSeasonAve = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['OverallPlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['OverallPlayerDashboard'][0]['GP']       #regular season average (playerdashboardbylastngames)
    aveAgainstTeam = endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()['OverallPlayerDashboard'][0]['PTS'] / endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()['OverallPlayerDashboard'][0]['GP']  #prop_type average against opposing team (playerdashboardbyopponent)
    #playoff_ave = 0     #if applicable (PlayerCareerStats['CareerTotalsPostSeason'])

    print("last 5: ", last5, " last 10: ", last10," Reg Season: ",regSeasonAve," Against Team: ", aveAgainstTeam, '\n')
    player[6] = (last5 + last10 + regSeasonAve + aveAgainstTeam) / 4

    player[7] = abs(float(player[6]) - float(player[3]))  # + = over margin, - = under margin

    #for both over & under
    if player[4] and player[5] in criteria:
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
    # if float(player[3]) < float(player[6]):
    #     player = np.append(player, ['over'])
    #     if str(player[4]) == '+100':
    #         if float(player[7]) <= -criteria['-110'] or criteria['-110'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 4'])
    #     if str(player[4]) == '-110':
    #         if float(player[7]) <= -criteria['-120'] or criteria['-120'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 3'])
    #
    #     if str(player[4]) == '-120':
    #         if float(player[7]) <= -criteria['-130'] or criteria['-130'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 2'])
    #
    #     if str(player[4]) == '-130':
    #         if float(player[7]) <= -criteria['-140'] or criteria['-140'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 1'])
    #     if str(player[4]) == '-140':
    #         if -criteria['-140'] <= float(player[7]) <= criteria['-140']:
    #             player = np.append(player, ['Confidence: 0'])
    #
    # else:
    #     player = np.append(player, ['under'])
    #     if str(player[5]) == '+100':
    #         if float(player[7]) <= -criteria['-110'] or criteria['-110'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 4'])
    #     if str(player[5]) == '-110':
    #         if float(player[7]) <= -criteria['-120'] or criteria['-120'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 3'])
    #     if str(player[5]) == '-120':
    #         if float(player[7]) <= -criteria['-130'] or criteria['-130'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 2'])
    #     if str(player[5]) == '-130':
    #         if float(player[7]) <= -criteria['-140'] or criteria['-140'] <= float(player[7]):
    #             player = np.append(player, ['Confidence: 1'])
    #     if str(player[5]) == '-140':
    #         if -criteria['-140'] <= float(player[7]) <= criteria['-140']:
    #             player = np.append(player, ['Confidence: 0'])


    print(player)
    return 0

def main():
    data = data_scraper()

    return

if __name__ == "__main__":
    main()