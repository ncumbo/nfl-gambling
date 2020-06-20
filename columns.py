import csv
import mysql.connector



def columns(column):
    game_week = column[3]
    teamname = column[4]
    home_v_away = column[5]
    q1 = column[6]
    q2 = column[7]
    q3 = column[8]
    q4 = column[9]
    ot = column[10]  # '' or a number
    team_score = column[11]
    opponent_score = column[12]
    first_down = column[13]
    rush_att = column[14]
    rush_yrds = column[15]
    rush_tds = column[16]
    pass_comp = column[17]
    pass_att = column[18]
    pass_yrds = column[19]
    pass_tds = column[20]
    ints = column[21]
    sacks_allowed = column[22]
    sack_allowed_yrds = column[23]
    passing_yrds = column[24]
    total_yrds = column[25]
    fumbles = column[26]
    fumbles_lost = column[27]
    turnovers = column[28]
    penalties = column[29]
    penalty_yrds = column[30]
    third_downs_made = column[31]
    third_downs_atp = column[32]
    forth_downs_made = column[33]
    forth_downs_atp = column[34]
    total_plays = column[35]
    time_of_possession = column[36]
    sacks = column[37]
    opponent_fumbles = column[38]
    def_fum_ret_td = column[39]
    int_ret_td = column[40]
    blockpunt_fg_ret_td = column[41]
    punt_kickoff_td = column[42]
    extra_pt_ret = column[43]
    d_2pt_con_ret = column[44]
    safeties= column[45]
    blocked_kick_punts = column[46]
    ints_made = column[47]
    opposing_2ptconv_made = column[48]
    opposing_extra_pt_made = column[49]
    opposing_fg_made = column[50]
    pts_allowed_by_defense = column[51]
    open_odds = column[52]
    open_spread = column[53]
    open_total = column[54]
    line_mvmt_1 = column[55]
    line_mvmt_2= column[56]
    line_mvmt_3= column[57]
    closing_odds = column[58]
    spread = column[59]
    ou = column[60]
    ml = column[61]  # 110 or -110
    ht_bet = column[62]
    return