import csv
import pandas as pd
import numpy as np
import glob

def basic():
    simple = []
    data = pd.read_csv("MLB Archives/mlb odds 2019.csv", delimiter=',')
    for team in data['Team'].unique():
        simple.append({'team': team, 'wins': 0, 'losses': 0, 'h_wins': 0, 'h_losses': 0, 'v_wins': 0, 'v_losses': 0,
                       'ml_profit': 0, 'h_ml_profit': 0, 'v_ml_profit': 0, 'over': 0, 'under': 0, 'h_over': 0,
                       'h_under': 0, 'v_over': 0, 'v_under': 0, 'ou_tie': 0, 'over_profit': 0, 'under_profit': 0,
                       'h_over_profit': 0, 'h_under_profit': 0, 'v_over_profit': 0, 'v_under_profit': 0})

    for file in glob.glob("MLB/MLB Archives/*.csv"):
        data = pd.read_csv(file, delimiter=',')
        data = data.drop_duplicates(subset="Team")

        for i in range(0, len(data), 2):
            v_teamdata = data.iloc[i]
            h_teamdata = data.iloc[i + 1]

            v_teamname = v_teamdata['Team']
            h_teamname = h_teamdata['Team']
            v_score = int(v_teamdata['Final'])
            h_score = int(h_teamdata['Final'])
            v_ml = v_teamdata['Close']
            h_ml = h_teamdata['Close']
            close_ou = float(v_teamdata['Close OU'])
            over_ml = v_teamdata[len(v_teamdata) - 1]
            under_ml = h_teamdata[len(h_teamdata) - 1]

            if h_teamname == 'LOS':
                home = next((item for item in simple if item['team'] == 'LAD'))
            else:
                home = next((item for item in simple if item['team'] == h_teamname))

            if v_teamname == 'LOS':
                away = next((item for item in simple if item['team'] == 'LAD'))
            else:
                away = next((item for item in simple if item['team'] == v_teamname))

            # ML
            lost_amt = -100
            if h_score < v_score:  # visitor win
                away['wins'] += 1
                away['v_wins'] += 1
                home['losses'] += 1
                home['h_losses'] += 1

                if int(v_ml) < 0:  # negative/favorite
                    away['ml_profit'] += round(100 * (100 / abs(int(v_ml))), 2)
                    away['v_ml_profit'] += round(100 * (100 / abs(int(v_ml))), 2)
                    home['ml_profit'] += lost_amt
                    home['h_ml_profit'] += lost_amt

                else:  # positive/dog
                    away['ml_profit'] = round(100 * (int(v_ml) / 100), 2)
                    away['v_ml_profit'] = round(100 * (int(v_ml) / 100), 2)
                    home['ml_profit'] += lost_amt
                    home['v_ml_profit'] += lost_amt

            if v_score < h_score:  # home win
                home['wins'] += 1
                home['h_wins'] += 1
                away['losses'] += 1
                away['v_losses'] += 1

                if int(h_ml) < 0:  # negative/favorite
                    home['ml_profit'] += round(100 * (100 / abs(int(h_ml))), 2)
                    home['h_ml_profit'] += round(100 * (100 / abs(int(h_ml))), 2)
                    away['ml_profit'] += lost_amt
                    away['v_ml_profit'] += lost_amt

                else:  # positive/dog
                    home['ml_profit'] = round(100 * (int(h_ml) / 100), 2)
                    home['h_ml_profit'] = round(100 * (int(h_ml) / 100), 2)
                    away['ml_profit'] = lost_amt
                    away['v_ml_profit'] = lost_amt

            # OVER/UNDERS
            if close_ou < h_score + v_score:  # over
                home['over'] += 1
                home['h_over'] += 1
                away['over'] += 1
                away['v_over'] += 1

                if int(over_ml) < 0:  # negative/favorite
                    home['over_profit'] += round(100 * (100 / abs(int(over_ml))), 2)
                    home['h_over_profit'] += round(100 * (100 / abs(int(over_ml))), 2)
                    away['over_profit'] += round(100 * (100 / abs(int(over_ml))), 2)
                    away['v_over_profit'] += round(100 * (100 / abs(int(over_ml))), 2)
                    home['under_profit'] += lost_amt
                    home['h_under_profit'] += lost_amt
                    away['under_profit'] += lost_amt
                    away['v_under_profit'] += lost_amt

                else:  # positive/dog
                    home['over_profit'] += round(100 * (int(over_ml) / 100), 2)
                    home['h_over_profit'] += round(100 * (int(over_ml) / 100), 2)
                    away['over_profit'] += round(100 * (int(over_ml) / 100), 2)
                    away['v_over_profit'] += round(100 * (int(over_ml) / 100), 2)
                    home['under_profit'] += lost_amt
                    home['h_under_profit'] += lost_amt
                    away['under_profit'] += lost_amt
                    away['v_under_profit'] += lost_amt


            elif h_score + v_score < close_ou:
                home['under'] += 1
                home['h_under'] += 1
                away['under'] += 1
                away['v_under'] += 1

                if int(under_ml) < 0:  # negative/favorite
                    home['under_profit'] += round(100 * (100 / abs(int(under_ml))), 2)
                    home['h_under_profit'] += round(100 * (100 / abs(int(under_ml))), 2)
                    away['under_profit'] += round(100 * (100 / abs(int(under_ml))), 2)
                    away['v_under_profit'] += round(100 * (100 / abs(int(under_ml))), 2)
                    home['over_profit'] += lost_amt
                    home['h_over_profit'] += lost_amt
                    away['over_profit'] += lost_amt
                    away['v_over_profit'] += lost_amt

                else:  # positive/dog
                    home['under_profit'] += round(100 * (int(under_ml) / 100), 2)
                    home['h_under_profit'] += round(100 * (int(under_ml) / 100), 2)
                    away['under_profit'] += round(100 * (int(under_ml) / 100), 2)
                    away['v_under_profit'] += round(100 * (int(under_ml) / 100), 2)
                    home['over_profit'] += lost_amt
                    home['h_over_profit'] += lost_amt
                    away['over_profit'] += lost_amt
                    away['v_over_profit'] += lost_amt
            else:
                home['ou_tie'] += 1
                away['ou_tie'] += 1

    simple = sorted(simple, key=lambda k: k['team'])
    for team in simple:
        team['ml_profit'] = round(team['ml_profit'], 2)
        team['h_ml_profit'] = round(team['h_ml_profit'], 2)
        team['v_ml_profit'] = round(team['v_ml_profit'], 2)
        team['over_profit'] = round(team['over_profit'], 2)
        team['under_profit'] = round(team['under_profit'], 2)
        team['h_over_profit'] = round(team['h_over_profit'], 2)
        team['h_under_profit'] = round(team['h_under_profit'], 2)
        team['v_over_profit'] = round(team['v_over_profit'], 2)
        team['v_under_profit'] = round(team['v_under_profit'], 2)
        print(team)
    print('\n')

def yearly():
    yearly = []
    years = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
    for yr in years:
        yearly.append({'year':yr,'fav_won':0,'dog_won':0,'over':0,'under':0, 'ou_ties':0})

    for file in glob.glob("MLB/MLB Archives/*.csv"):
        file_year = file.split(' ')[3].split('.')[0]
        data = pd.read_csv(file, delimiter=',')
        data = data.drop_duplicates(subset="Team")
        print(file_year)

        for i in range(0, len(data), 2):
            v_teamdata = data.iloc[i]
            h_teamdata = data.iloc[i + 1]

            v_score = int(v_teamdata['Final'])
            h_score = int(h_teamdata['Final'])
            v_ml = v_teamdata['Close']
            h_ml = h_teamdata['Close']
            close_ou = float(v_teamdata['Close OU'])

            year_odds = next((item for item in yearly if item['year'] == int(file_year)))

            #FAV
            if h_score < v_score:  # visitor win
                if int(v_ml) < 0:  # negative/favorite
                    year_odds['fav_won'] += 1
                else:  # positive/dog
                    year_odds['dog_won'] +=1
            if v_score < h_score:  # home win
                if int(h_ml) < 0:  # negative/favorite
                    year_odds['fav_won'] += 1
                else:  # positive/dog
                    year_odds['dog_won'] += 1

            #OVER/UNDER
            if close_ou < h_score + v_score:  # over
                year_odds['over'] +=1

            elif h_score + v_score < close_ou:
                year_odds['under'] +=1

            else:
                year_odds['ou_ties'] +=1

    for each in yearly:
        print(each)

def main():
    basic()
    yearly()

    return 0

if __name__ == "__main__":
    main()