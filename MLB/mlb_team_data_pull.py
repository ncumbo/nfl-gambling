from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import numpy as np

def data_scrape(date):
    #link = "https://www.baseball-reference.com/boxes/ANA/ANA202008290.shtml"
    link = "https://www.baseball-reference.com/boxes/DET/DET202008291.shtml"
    #page = requests.get(link, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})
    driver = webdriver.Firefox()
    driver.get(link)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    game_date = [["Date", "H/A"], [date, "A"], [date, "H"]]

    #Scoreboard Metadata
    scoreboard_meta = str(page.find_all("div", class_="scorebox_meta")[0]).split("<div>")
    print(scoreboard_meta)
    if "doubleheader" in scoreboard_meta[7]:
        doubleheader_or_not = 2
    else:
        doubleheader_or_not = 0

    print(doubleheader_or_not)
    game_date[0].append("Gametime")
    game_date[0].append("Duration")
    game_date[0].append("Day/Night")
    game_date[0].append("Ground Condition")
    game_date[1].append(scoreboard_meta[2].split(" ")[2] + scoreboard_meta[2].split(" ")[3])
    game_date[1].append(str(scoreboard_meta[4].split(" ")[2])[:-6])
    game_date[1].append(scoreboard_meta[5].split(" ")[0])
    game_date[1].append(str(scoreboard_meta[5].split(" ")[3])[:-6])
    game_date[2].append(scoreboard_meta[2].split(" ")[2] + scoreboard_meta[2].split(" ")[3])
    game_date[2].append( str(scoreboard_meta[4].split(" ")[2])[:-6])
    game_date[2].append(scoreboard_meta[5].split(" ")[0])
    game_date[2].append(str(scoreboard_meta[5].split(" ")[3])[:-6])

    #Teamnames
    game_date[0].append("Team")
    game_date[1].append(str(page.find_all("div", class_="box")[0]).split("h1")[1].split(" ")[0][1:] + " " + str(page.find_all("div", class_="box")[0]).split("h1")[1].split(" ")[1])
    game_date[2].append(str(page.find_all("div", class_="box")[0]).split("h1")[1].split(" at ")[1].split("Box Score")[0])

    #Other Info - Stuck here
    other_info = str(page.find_all(class_=["section_content"])[2])
    game_date[0].append("HP Umpire")
    game_date[0].append("Tempature")
    game_date[0].append("Weather Conditions")
    game_date[0].append("Wind Speed")
    game_date[1].append(other_info.split("HP - ")[1].split(",")[0]) #works
    game_date[1].append(other_info.split("<div><strong>Start Time Weather:</strong> ")[1].split("°")[0])
    game_date[1].append(other_info.split("</strong>")[5].split(", ")[2])
    game_date[1].append(other_info.split("Wind ")[1].split("mph")[0])
    game_date[2].append(other_info.split("HP - ")[1].split(",")[0]) #works
    game_date[2].append(other_info.split("<div><strong>Start Time Weather:</strong> ")[1].split("°")[0])
    game_date[2].append(other_info.split("</strong>")[5].split(", ")[2])
    game_date[2].append(other_info.split("Wind ")[1].split("mph")[0])

    #Innings Table    (Need to account for 7 inning games)
    table = str(page.find("table", {"class": "linescore nohover stats_table no_freeze"}).find("tbody")).split("<td class=\"center\">")
    table.pop(0)
    table = [x for x in table if "div" not in x]
    home_in = []
    away_in = []
    tr_index = 0
    for a_inning in range(len(table) + 1):
        if "</tr>" not in table[a_inning]:
            away_in.append(str(table[a_inning]).split("</")[0])
        else:
            away_in.append(str(table[a_inning]).split("</")[0])
            tr_index = a_inning
            break

    for h_inning in range(tr_index + 1, len(table)):
        home_in.append(str(table[h_inning]).split("</")[0])

    a_extras = 0
    h_extras = 0
    for inning in range(len(away_in) - 3):  #only 9+ innings
        if home_in[inning] == "X":
            home_in[inning] = 0

        #check if there was extras in a 7 inning game, if len_of_game == 7
        if doubleheader_or_not == 2:
            x = 8
        else:
            x = 10

        if x <= inning:
            a_extras = a_extras + away_in[inning]
            h_extras = h_extras + home_in[inning]
        else:
            game_date[0].append(str(inning + 1))
            game_date[1].append(away_in[inning])
            game_date[2].append(home_in[inning])

    #append 0's to inning 8 & 9 if len() of doubleheader = 7 or 8
    if (len(away_in) - 3) == 7:
        game_date[0].append("8")
        game_date[0].append("9")
        game_date[1].append(0)  #8th
        game_date[1].append(0)  #9th
        game_date[2].append(0)  #8th
        game_date[2].append(0)  #9th
    if (len(away_in) - 3) == 8:
        game_date[0].append("9")
        game_date[1].append(0)  #9th
        game_date[2].append(0)  #9th

    #Extras
    game_date[0].append("Extras")
    game_date[1].append(a_extras)
    game_date[2].append(h_extras)

    #Score/Hits/Errors/Total Innings
    game_date[0].append("Final Score")
    game_date[0].append("Total Hits")
    game_date[0].append("Total Errors")
    game_date[0].append("Total Innings")
    game_date[1].append(away_in[len(away_in) - 3])
    game_date[1].append(away_in[len(away_in) - 2])
    game_date[1].append(away_in[len(away_in) - 1])
    game_date[1].append(len(away_in) - 3)
    game_date[2].append(home_in[len(home_in) - 3])
    game_date[2].append(home_in[len(home_in) - 2])
    game_date[2].append(home_in[len(home_in) - 1])
    game_date[2].append(len(home_in) - 3)

    print(table)
    print(away_in)
    print(home_in)
    print(game_date[0])
    print(game_date[1])
    print(game_date[2])

    #Vegas
    link = "https://www.vegasinsider.com/mlb/odds/las-vegas/line-movement/twins-@-tigers.cfm/date/08-29-20/time/1310"
    driver = webdriver.Firefox()
    driver.get(link)
    page = BeautifulSoup(driver.page_source, 'html.parser')

    #Get "CAESARS/HARRAH'S LINE MOVEMENTS" table
    #Get first occurance of each
    #Get last occurance of each

    # bball_ref_link = "https://www.baseball-reference.com/boxes/?year=" + date[6:] + "&month=" + date[:2] + "&day=" + date[3:5]
    # page = requests.get(bball_ref_link, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})
    # driver = webdriver.Firefox()
    # driver.get(bball_ref_link)
    # content = BeautifulSoup(page.content, 'html.parser')
    # for each_game in content.find_all('div', {"class" :"game_summary nohover"}):    #For each game
    #     #print(each_game)
    #     link = each_game.find('td', {"class":"right gamelink"})
    #     driver.find_element_by_link_text('Final').click()
    #
    #     game_date = {(date,"A"),(date, "H")}
    #     page = BeautifulSoup(driver.page_source, 'html.parser')
    #
    #
    #     linescore = page.find_all('div', {"class":"linescore_wrap"})
    #     print(game_date)
    #     print(linescore)
    #     # for row in linescore.find_all('tr'):
    #     #     cols = row.find_all('td')
    #     #     cols = [ele.text.strip() for ele in cols]
    #     #     print(cols)
    #
    #     #driver.find_element_by_link_text('MLB Scores & Standings on this Day').click()
    #     break
        #for each game, click expand

    #print(content.get_text())

def scrape_currentday_odds():
    return

def main():
    date = "08/30/2020" #input("Enter date as mm/dd/yyyy: ")
    data_scrape(date)

    return

if __name__ == "__main__":
    main()


    #Pitching Stats: ERA, WHIP, G/F Rate, K/9, HR/9, Run Support Ave, BABIP, Prev Start
    #Hitting Stats: Team Performance v R/L

    #Game: Date, Game-Time, Umpire,Team, H/A, SP, Inning Score, Final, ML, RL, RL ML, OU, OU ML, # pitchers used in game
    #Current Statistics:  ERA, WHIP, G/F Rate, K/9, HR/9

    #save the day to a database
    #given a day, continue searching until you reach that day
        #for every game in that day

    #game stats: https://www.baseball-reference.com/boxes/?year=2020&month=07&day=24
    #betting stats: