import csv
import pandas as pd
import numpy as np
import glob
import os

def basic():
    numGoals = {}
    for file in glob.glob("NHL Archives/*.csv"):
        data = pd.read_csv(file, delimiter=',')
        for i in range(0, len(data), 2):
            v_teamdata = data.iloc[i]
            h_teamdata = data.iloc[i + 1]
            v_teamname = v_teamdata['Team']
            h_teamname = h_teamdata['Team']
            v_score = int(v_teamdata['Final'])
            h_score = int(h_teamdata['Final'])

            #if the outcome or the opposite of the outcome isnt in the dictionary, then add it in and add 1
            num = int(v_score) + int(h_score)
            if str(num) not in numGoals:
                numGoals.update({str(num): 1})
            else:
                numGoals[str(num)] = numGoals[str(num)] + 1


    print(numGoals)



def yearly():
    yearly = []
    years = ["2007-08","2008-09","2009-10","2010-11","2011-12","2012-13","2013-14","2014-15","2015-16","2016-17","2017-18","2018-19","2019-20"]
    for yr in years:
        yearly.append({'year':yr})

    for file in glob.glob("NHL Archives/*.csv"):
        file_year = file.split(' ')[3].split('.')[0]
        data = pd.read_csv(file, delimiter=',')
        print(file_year)

        for i in range(0, len(data), 2):
            v_teamdata = data.iloc[i]
            h_teamdata = data.iloc[i + 1]
            v_score = int(v_teamdata['Final'])
            h_score = int(h_teamdata['Final'])

            year_odds = next((item for item in yearly if item['year'] == str(file_year)))   #finds the dictionary with the odds
            num = int(v_score) + int(h_score)

            if str(num) not in yearly:
                year_odds[str(num)] = 1
            else:
                year_odds[str(num)] += 1

    print(yearly)

def main():
    basic()
    #yearly()

    return 0

if __name__ == "__main__":
    main()