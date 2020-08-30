from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import numpy as np

def main():
    #Pitching Stats: ERA, WHIP, G/F Rate, K/9, HR/9, Run Support Ave, BABIP, Prev Start
    #Hitting Stats: Team Performance v R/L

    #Game: Date, Game-Time, Umpire,Team, H/A, SP, Inning Score, Final, ML, RL, RL ML, OU, OU ML, # pitchers used in game
    #Current Statistics:  ERA, WHIP, G/F Rate, K/9, HR/9

    #save the day to a database
    #given a day, continue searching until you reach that day
        #for every game in that day

    #game stats: https://www.baseball-reference.com/boxes/?year=2020&month=07&day=24
    #betting stats:

    page = requests.get("https://www.baseball-reference.com/boxes/?year=2020&month=07&day=24", {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})
    driver = webdriver.Firefox()
    driver.get("https://www.baseball-reference.com/boxes/?year=2020&month=07&day=24")
    #content = BeautifulSoup(driver.page_source, 'html.parser')
    content = BeautifulSoup(page.content, 'html.parser')
    for each_game in content.find_all('div', {"class" :"game_summary nohover"}):
        #print(each_game)
        link = each_game.find('td', {"class":"right gamelink"})
        driver.find_element_by_link_text('Final').click()

        away = []
        home = []
        page = BeautifulSoup(driver.page_source, 'html.parser')
        linescore = each_game.find_all('div', {"class":"linescore_wrap"})
        print(linescore)
        for row in linescore.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            print(cols)

        #driver.find_element_by_link_text('MLB Scores & Standings on this Day').click()
        break
        #for each game, click expand

    #print(content.get_text())

    return

if __name__ == "__main__":
    main()