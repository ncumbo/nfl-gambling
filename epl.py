import pandas as pd
import nba_api
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

def past_5_games_all():
    accepted_bets = []
    bet_line = []    #[Date, Team, Opponent, 1H_Line, Num_1H_Goals, 1H ML]

    #driver = webdriver.Firefox()
    #driver.get("http://www.espn.com/soccer/scoreboard")
    #content = BeautifulSoup(driver.page_source, 'html.parser')

    page = requests.get("http://www.espn.com/soccer/scoreboard")
    content = BeautifulSoup(page.content, "html.parser")
    print(content)

    #go to day before
    #yesterday_button = driver.find_element_by_class_name("slick-prev slick-arrow")
    #yesterday_button.click()    #click link

    #page = requests.get("http://www.espn.com/soccer/scoreboard", {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'})

    #Use Selenium
    #For each of last 5 pages
        #For every score board gather data

    #Get lines

    #Get Results


    return 0


def main():
    data = past_5_games_all()
    return

if __name__ == "__main__":
    main()