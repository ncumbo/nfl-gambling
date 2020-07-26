import pandas as pd
from nba_api.stats.static import players
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
    # page = requests.get("", {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})
    # content = BeautifulSoup(page.content, 'html.parser')
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
    player = player_prop("Lakers","Lebron James","Points", 27.5, "-130", "-110")
    #player = player_prop("Jazz","Rudy Gobert", "Points", 15.5, "-120", "-120")
    #check to see if player prop is acceptable and within the margins
    x = margin(player)

    return 0

def margin(data):
    criteria = {'+100': 4, '-110': 3, '-120': 2, '-130': 1,'-140': 0.5}  # Subject to change depending on ML implementation

    playerID = players.find_players_by_full_name(data.player_name)[0]['id']      #find player reference number in static
    opponentID = endpoints.PlayerNextNGames(player_id=playerID).get_normalized_dict()['NextNGames'][0]['VISITOR_TEAM_ID']

    #Only accounting for ppg. change variable type in each
    last5 = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last5PlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last5PlayerDashboard'][0]['GP']
    last10 = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last10PlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['Last10PlayerDashboard'][0]['GP']               #last 10 games (playerdashboardbylastngames)
    regSeasonAve = endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['OverallPlayerDashboard'][0]['PTS']/endpoints.PlayerDashboardByLastNGames(player_id=playerID).get_normalized_dict()['OverallPlayerDashboard'][0]['GP']       #regular season average (playerdashboardbylastngames)

    print(endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()['OverallPlayerDashboard'])
    # aveAgainstTeam = endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()['OverallPlayerDashboard'][0]['PTS'] / endpoints.PlayerDashboardByOpponent(player_id=playerID, opponent_team_id=opponentID).get_normalized_dict()['OverallPlayerDashboard'][0]['GP']  #prop_type average against opposing team (playerdashboardbyopponent)
    # #playoff_ave = 0     #if applicable (PlayerCareerStats['CareerTotalsPostSeason'])
    #
    # aveProp = (last5 + last10 + regSeasonAve + aveAgainstTeam) / 4
    # marg = abs(data.prop_total - aveProp)   #+/-
    # print(marg)
    # if any(data.over_ml in i for i in criteria):
    #     if criteria[data.over_ml] == 0.5:
    #         if -criteria[data.over_ml] <= marg <= criteria[data.over_ml]:
    #             data.over_or_under == "over"
    #
    #     elif criteria[data.over_ml] == 1:
    #         if -criteria[data.over_ml] <= marg <= -0.5 and 0.5 <= marg <= criteria[data.over_ml]:
    #             data.over_or_under == "over"
    #     else:
    #         if -criteria[data.over_ml] <= marg <= (-criteria[data.over_ml] + 1) and (-criteria[data.over_ml] - 1) <= marg <= criteria[data.over_ml]:
    #             data.over_or_under == "over"
    # ###
    # if any(data.under_ml in i for i in criteria):
    #     if criteria[data.under_ml] == 0.5:
    #         if -criteria[data.under_ml] <= marg <= criteria[data.under_ml]:
    #             if data.over_or_under == "over":
    #                 data.over_or_under = "both"
    #             else:
    #                 data.over_or_under = "under"
    #
    #     elif criteria[data.under_ml] == 1:
    #         if -criteria[data.under_ml] <= marg <= -0.5 and 0.5 <= marg <= criteria[data.under_ml]:
    #             if data.over_or_under == "over":
    #                 data.over_or_under = "both"
    #             else:
    #                 data.over_or_under = "under"
    #     else:
    #         if -criteria[data.under_ml] <= marg <= (-criteria[data.under_ml] + 1) and (-criteria[data.under_ml] - 1) <= marg <= criteria[data.under_ml]:
    #             if data.over_or_under == "over":
    #                 data.over_or_under = "both"
    #             else:
    #                 data.over_or_under = "under"

    print(data)
    return 0

def main():
    data = data_scraper()

    return

if __name__ == "__main__":
    main()