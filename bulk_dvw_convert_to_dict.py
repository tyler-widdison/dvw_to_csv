
#def multi(path = 'C:\\Users\\Tyler.Widdison\\Desktop\\Python\\test'):
#    results = []
#    for dvw_file in os.listdir(path):
#        results.append(all_events(f'{path}\\{dvw_file}'))
#    return results

#def find_first_serve(lines):
#    for idx, line in enumerate(lines):
#        if line[0:4] in ['a01S', 'a02S', '*01S', '*02S']:
#            return idx

def player_parse(file):
    team_1_data = linecache.getline(file, 19)
    team_1_split_data = team_1_data.split(';')
    team_one_id = team_1_split_data[0]
    team_one_name = team_1_split_data[1]
    team_2_data = linecache.getline(file, 20)
    team_2_split_data = team_2_data.split(';')
    team_two_id = team_2_split_data[0]
    team_two_name = team_2_split_data[1]
    player_1_team_1_data = linecache.getline(file, 33)
    player_1_split_data = player_1_team_1_data.split(';')
    player_one_team_one_number = player_1_split_data[2]
    player_one_team_one_id = player_1_split_data[8]
    player_one_team_one_name = player_1_split_data[10] + ' ' + player_1_split_data[9]
    player_2_team_1_data = linecache.getline(file, 34)
    player_2_split_data = player_2_team_1_data.split(';')
    player_two_team_one_number = player_2_split_data[2]
    player_two_team_one_id = player_2_split_data[8]
    player_two_team_one_name = player_2_split_data[10] + ' ' + player_2_split_data[9]
    player_1_team_2_data = linecache.getline(file, 36)
    player_1_split_data_2 = player_1_team_2_data.split(';')
    player_one_team_two_number = player_1_split_data_2[2]
    player_one_team_two_id = player_1_split_data_2[8]
    player_one_team_two_name = player_1_split_data_2[10] + ' ' + player_1_split_data_2[9]
    player_2_team_2_data = linecache.getline(file, 37)
    player_2_split_data_2 = player_2_team_2_data.split(';')
    player_two_team_two_number = player_2_split_data_2[2]
    player_two_team_two_id = player_2_split_data_2[8]
    player_two_team_two_name = player_2_split_data_2[10] + ' ' + player_2_split_data_2[9]
    return [
        {
            'id': player_one_team_one_id,
            'name': player_one_team_one_name,
            'player_number': player_one_team_one_number,
            'team_id': team_one_id,
            'team': team_one_name
        },
        {
            'id': player_two_team_one_id,
            'name': player_two_team_one_name,
            'player_number': player_two_team_one_number,
            'team_id': team_one_id,
            'team': team_one_name
        },
        {
            'id': player_one_team_two_id,
            'name': player_one_team_two_name,
            'player_number': player_one_team_two_number,
            'team_id': team_two_id,
            'team': team_two_name
        },
        {
            'id': player_two_team_two_id,
            'name': player_two_team_two_name,
            'player_number': player_two_team_two_number,
            'team_id': team_two_id,
            'team': team_two_name
        },
    ]

def all_events(file):
    all_events = []
    home_score = '00'
    away_score = '00'
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if 'az1' in line:
                for line in f:
                    line = line.split(';')
                    skill = convert_event(file, line, home_score, away_score)
                    all_events.append(skill)
                    if skill['descrption'] == 'point':
                        home_score = skill['home_score']
                        away_score = skill['away_score']
                return all_events

def convert_event(file, line, home_score, away_score):
    single_event = {
        'xycoordinate': '',
        'descrption': '',
        'details': '',
        'grade': '',
        'timestamp': '',
        'player_id': '',
        'teamid': '',
        'home_teamid': '',
        'away_teamid': '',
        'name': '',
        'player_number': '',
        'home_score': home_score,
        'away_score': away_score,
        'block': '',
        'attack_combo': '',
        'match_id': '',
        'start_coordinate': '',
        'mid_coordinate': '',
        'end_coordinate':'',
        'set_number': '',
        'net_let': '',
        'dig_details': ''
        #'fbso': ''
        #'trans': ''
    }
    first_portion = line[0]
    if first_portion[-1:] == 'N':
        single_event['net_let'] = 'let'
    if first_portion[1:2] == 'p':
        time_value = line[19]
    else:
        time_value = line[12]
    single_event['start_coordinate'] = line[4]
    single_event['mid_coordinate'] = line[5]
    single_event['end_coordinate'] = line[6]
    single_event['set_number'] = line[8]
    single_event['timestamp'] = time_value
    descrption(first_portion, single_event)
    grade(first_portion, single_event)
    player_info(file, first_portion, single_event)
    attacking_details(first_portion, single_event)
    set_details(first_portion, single_event)
    reception_details(first_portion, single_event)
    serve_details(first_portion, single_event)
    dig_details(first_portion, single_event)
    match_id(file, single_event)
    if first_portion[0:2] == 'ap' or first_portion[0:2] == '*p':
        score_split = first_portion[2:].split(':')
        single_event['home_score'] = score_split[0]
        single_event['away_score'] = score_split[1]
    return single_event

def descrption(first_portion, single_event):
    if first_portion[3:4] == 'S':
        single_event['descrption'] = 'serve'
    if first_portion[3:4] == 'R':
        single_event['descrption'] = 'reception'
    if first_portion[3:4] == 'E':
        single_event['descrption'] = 'set'
    if first_portion[3:4] == 'A':
        single_event['descrption'] = 'attack'
    if first_portion[3:4] == 'B':
        single_event['descrption'] = 'block'
    if first_portion[3:4] == 'D':
        single_event['descrption'] = 'dig'
    if first_portion[3:4] == 'F':
        single_event['descrption'] = 'free_ball'
    if first_portion[1:2] == 'p':
        single_event['descrption'] = 'point'

def match_id(file, single_event):
    with open(file, 'r', encoding='utf-8') as f:
        lin = f.readlines()
        single_event['match_id'] = lin[21].split(';')[5]

def match_id_two(file, single_event):
    with open(file, 'r', encoding='utf-8') as f:
        names = file
        single_event['match_id'] = names.split('usa')[0].split('-')[2][2:]

#def set_number(file, single_event):
#    for lin in open(file, 'r', encoding='utf-8').readlines():
#        test1 = lin.split('00.06.35.59')
#        single_event['set_number'] = test1[1][1:2]

def grade(first_portion, single_event):
    if first_portion[5:6] == '#':
        single_event['grade'] = '#'
    if first_portion[5:6] == '!':
        single_event['grade'] = '!'
    if first_portion[5:6] == '-':
        single_event['grade'] = '-'
    if first_portion[5:6] == '/':
        single_event['grade'] = '/'
    if first_portion[5:6] == '=':
        single_event['grade'] = '='
    if first_portion[5:6] == '+':
        single_event['grade'] = '+'

def player_info(file, first_portion, single_event):
    team_1_data = linecache.getline(file, 19)
    team_1_split_data = team_1_data.split(';')
    team_one_id = team_1_split_data[0]
    team_2_data = linecache.getline(file, 20)
    team_2_split_data = team_2_data.split(';')
    team_two_id = team_2_split_data[0]
    player_1_team_1_data = linecache.getline(file, 33)
    player_1_split_data = player_1_team_1_data.split(';')
    player_one_team_one_number = player_1_split_data[2]
    player_one_team_one_id = player_1_split_data[8]
    player_one_team_one_name = player_1_split_data[10] + ' ' + player_1_split_data[9]
    player_2_team_1_data = linecache.getline(file, 34)
    player_2_split_data = player_2_team_1_data.split(';')
    player_two_team_one_number = player_2_split_data[2]
    player_two_team_one_id = player_2_split_data[8]
    player_two_team_one_name = player_2_split_data[10] + ' ' + player_2_split_data[9]
    player_1_team_2_data = linecache.getline(file, 36)
    player_1_split_data_2 = player_1_team_2_data.split(';')
    player_one_team_two_number = player_1_split_data_2[2]
    player_one_team_two_id = player_1_split_data_2[8]
    player_one_team_two_name = player_1_split_data_2[10] + ' ' + player_1_split_data_2[9]
    player_2_team_2_data = linecache.getline(file, 37)
    player_2_split_data_2 = player_2_team_2_data.split(';')
    player_two_team_two_number = player_2_split_data_2[2]
    player_two_team_two_id = player_2_split_data_2[8]
    player_two_team_two_name = player_2_split_data_2[10] + ' ' + player_2_split_data_2[9]
    if first_portion[0:1] == '*':
        single_event['teamid'] = unidecode(team_one_id)
    if first_portion[0:1] == 'a':
        single_event['teamid'] = unidecode(team_two_id)
    if first_portion[0:1] == '*':
        single_event['home_teamid'] = unidecode(team_one_id)
    if first_portion[0:1] == 'a':
        single_event['away_teamid'] = unidecode(team_two_id)
    if first_portion[0:1] == 'a' and first_portion[1:3] == '01':
        single_event['name'] = unidecode(player_one_team_two_name)
    if first_portion[0:1] == 'a' and first_portion[1:3] == '02':
        single_event['name'] = unidecode(player_two_team_two_name)
    if first_portion[0:1] == '*' and first_portion[1:3] == '01':
        single_event['name'] = unidecode(player_one_team_one_name)
    if first_portion[0:1] == '*' and first_portion[1:3] == '02':
        single_event['name'] = unidecode(player_two_team_one_name)
    if first_portion[0:1] == 'a' and first_portion[1:3] == '01':
        single_event['player_id'] = player_one_team_two_id
    if first_portion[0:1] == 'a' and first_portion[1:3] == '02':
        single_event['player_id'] = player_two_team_two_id
    if first_portion[0:1] == '*' and first_portion[1:3] == '01':
        single_event['player_id'] = player_one_team_one_id
    if first_portion[0:1] == '*' and first_portion[1:3] == '02':
        single_event['player_id'] = player_two_team_one_id
    if first_portion[0:1] == 'a' and first_portion[1:3] == '01':
        single_event['player_number'] = player_one_team_two_number
    if first_portion[0:1] == 'a' and first_portion[1:3] == '02':
        single_event['player_number'] = player_two_team_two_number
    if first_portion[0:1] == '*' and first_portion[1:3] == '01':
        single_event['player_number'] = player_one_team_one_number
    if first_portion[0:1] == '*' and first_portion[1:3] == '02':
        single_event['player_number'] = player_two_team_one_number

def attacking_details(first_portion, single_event):
    # getting block 
    if first_portion[3:4] == 'A' and first_portion[13] == '3':
        single_event['block'] = 'jump_line'
    if first_portion[3:4] == 'A' and first_portion[13] == '4':
        single_event['block'] = 'jump_angle'
    if first_portion[3:4] == 'A' and first_portion[13] == '2':
        single_event['block'] = 'angle'
    if first_portion[3:4] == 'A' and first_portion[13] == '1':
        single_event['block'] = 'line'
    if first_portion[3:4] == 'A' and first_portion[13] == '0':
        single_event['block'] = 'peel'

    # get attack type with no let
    if first_portion[3:4] == 'A' and first_portion[12] == 'H':
        single_event['details'] = 'hard'
    if first_portion[3:4] == 'A' and first_portion[12] == 'P':
        single_event['details'] = 'shot'
    if first_portion[3:4] == 'A' and first_portion[12] == 'T':
        single_event['details'] = 'pokey'

    # get attack combo
    if first_portion[3:4] == 'A':
        single_event['attack_combo'] = first_portion[6:8]      
    if first_portion[3:4] == 'A':
        single_event['xycoordinate'] = first_portion[10:12]    

def dig_details(first_portion, single_event):
    if first_portion[3:4] == 'D' and first_portion[-1:] == 'E':
        single_event['dig_details'] = 'emergency'
    if first_portion[3:4] == 'D' and first_portion[-1:] == 'S':
        single_event['dig_details'] = 'on_spike'
    if first_portion[3:4] == 'D' and first_portion[-1:] == 'B':
        single_event['dig_details'] = 'after_block'

def set_details(first_portion, single_event):
    if first_portion[3:4] == 'E':
        single_event['details'] = first_portion[8:9]
    if first_portion[3:4] == 'E':
        single_event['xycoordinate'] = first_portion[10:12]

def reception_details(first_portion, single_event):
    if first_portion[3:4] == 'R' and first_portion[-1] == 'R':
        single_event['details'] = 'right'
    if first_portion[3:4] == 'R' and first_portion[-1] == 'L':
        single_event['details'] = 'left'
    if first_portion[3:4] == 'R' and first_portion[-1] == 'M':
        single_event['details'] = 'middle'
    if first_portion[3:4] == 'R' and first_portion[-1] == 'W':
        single_event['details'] = 'low'
    if first_portion[3:4] == 'R' and first_portion[-1] == 'O':
        single_event['details'] = 'overhead'
    if first_portion[3:4] == 'R':
        single_event['xycoordinate'] = first_portion[10:12]

def serve_details(first_portion, single_event):
    if first_portion[3:5] == 'SH':
        single_event['details'] = 'standing_float_far'
    if first_portion[3:5] == 'ST':
        single_event['details'] = 'standing_float_near'
    if first_portion[3:5] == 'SO':
        single_event['details'] = 'underhand'
    if first_portion[3:5] == 'SM':
        single_event['details'] = 'jump_float'
    if first_portion[3:5] == 'SQ':
        single_event['details'] = 'jump_serve'
    if first_portion[3:4] == 'S':
        single_event['xycoordinate'] = first_portion[10:12]

#def main(path = 'C:\\Users\\Tyler.Widdison\\Desktop\\Python\\test'):
#    all_the_events = multi(path)
#    print(all_the_events)


import linecache
from itertools import islice
import pandas as pd
import re
import pprint
from pathlib import Path
import os
import json
import csv
import numpy as np
from pandas.io.json import json_normalize   
from unidecode import unidecode

file_names = []
for file in os.listdir("C:\\Users\\Tyler.Widdison\\Desktop\\Python\\"):
    try:
        if file.endswith(".dvw"):
            file_names.append(all_events(file))
    except:
        print(file)


from funcy import join
dfs = join(file_names)

df = pd.DataFrame(dfs)
df['start_zone'] = df['xycoordinate'].astype(str).str[0]
df['start_subzone'] = df['xycoordinate'].astype(str).str[1]
df['start_zone'] = pd.to_numeric(df['start_zone'], errors = 'ignore')
df = df[df['descrption']!='']
df['home_score'] = df['home_score'].apply(lambda x : x.zfill(2))
df['away_score'] = df['away_score'].apply(lambda x : x.zfill(2))
df = df.replace(r'^\s*$', np.nan, regex=True)
df['home_teamid'] = df['home_teamid'].fillna(method='ffill')
df['away_teamid'] = df['away_teamid'].fillna(method='ffill')
df['home_teamid'] = df['home_teamid'].fillna(method='bfill')
df['away_teamid'] = df['away_teamid'].fillna(method='bfill')
df['mid_coordinate'] = df['mid_coordinate'].str.replace('-1-1','').replace('', np.nan, regex=True)
df['end_coordinate'] = df['end_coordinate'].str.replace('-1-1','').replace('', np.nan, regex=True)



df.to_csv('test333.csv')


df = pd.DataFrame()
df['ID'] = dat[ID].astype(str)
df['period'] = dat[period_id].astype(int)
df['player_name'] = dat[player]
df['team_name'] = dat[team]
df['time'] = dat[time].astype(int)
df['metric'] = dat[metric_val]














#'Test' 
    #with open('attempt_2.json', 'w') as outfile:
    #    json.dump(data, outfile)
    #
    #with open('attempt_2.json', 'r') as read_file:
    #    ddd = json.load(read_file)
    #
    #
    #df = pd.DataFrame(test)
    #
    #df.replace(r'^\s*$', np.NAN, regex=True)
    #
    #df.to_csv('boom.csv')
    #
    #import matplotlib.pyplot as plt
    #import seaborn as sns
    #import numpy as np
    #sns.set()
    #%matplotlib inline
    #lin = f.readlines()
    #match_id_line = lin[21]
    #match_id_split = match_id_line.split(';')
    #match_id = match_id_split[5]

    #
    #
    ##data = all_events(file)
    #data = multi()
    ##main()
    ##
    ###descrption(first_portion, single_event)
    ###
    ###def convertToDescription(firstPortion):
    ###    skillAbbreviation = firstPortion[3:4]
    ###    pointAbbreviation = firstPortion[1:2]
    ###    if skillAbbreviation == 'S':
    ###        return 'serve'
    ###    if skillAbbreviation == 'R':
    ###        return 'reception'
    ###    #...
    ###    if pointAbbreviation == 'p':
    ###        return 'point'
    ###
    ###single_event['description'] = convertToDescription(first_portion)
    #
    #attacks = [e for e in data if e['descrption'] == 'attack']
    #
    #
    ##import re
    ##import pprint
    ###from pathlib import Path
    ###
    ###resumes_dir = Path("test")
    ###for path in resumes_dir.glob("*.dvw"):
    ###    with path.open() as f:
    ###        lines = islice(f, 73, 5000)
    ###        for file_ in lines:
    ###            line = file_.split(';')
    ###            print(line)
    ##
    #blocks = []
    #allbe = [p for p in data if p['descrption'] in ['serve', 'receive', 'set', 'attack', 'block', 'dig']]
    #for block in allbe:
    #    player = f"{block['teamid']} {block['player_number']} {block['name']} - "
    #    details = f"{block['descrption']} {block['details']}"
    #    grade = (block['grade'])
    #    blocks.append([player, details, grade])
    #




    #fig=plt.figure() #set up the figures
    #fig.set_size_inches(7, 5)
    #ax=fig.add_subplot(1,1,1)
    #draw_pitch(ax) #overlay our different objects on the pitch
    #plt.ylim(-2, 82)
    #plt.xlim(-2, 122)
    #plt.axis('off')
    #plt.show()
    #
    #from matplotlib import pyplot as plt
    #from matplotlib.patches import Rectangle
    #someX, someY = 0.5, 0.5
    #fig,ax = plt.subplots()
    #currentAxis = plt.gca()
    #currentAxis.add_patch(Rectangle((someX - 0.1, someY - 0.1), 0.2, 0.2,
    #                      alpha=1, facecolor='none'))


    #newl = []
    #with open('&test.dvw') as lines:
    #    f = lines.readlines()
    #    line = f.split(';')
    #
    #fbso = 'fbso'
    #
    #test = []
    #with open('&test.dvw', 'r', encoding='utf-8') as f:
    #    for file_ in f:
    #        line = file_.split(';')
    #        first = line[0]
    #        if first[3:4] == 'S':
    #
    #            
    #filne = '&test.dvw'
    #
    #with open(filne, 'r+') as f:
    #    for line in f:
    #        if line[3:4] == 'S':
    #            next(f, '2')         
    #
    #s = open('&test.dvw')
    #
    #def daten(s): 
    #   s = iter(s)
    #   for line in s:  
    #       if line[3:4] == 'S':
    #            return [line, next(s), next(s), next(s)]
    #   else:
    #       raise SomeException
    #
    #for test in daten(s):
    #    print(test)
    #
    #
    #daten(s)
    #
    #    for idx, line in enumerate(lines):
    #        if line[0:4] in ['a01S', 'a02S', '*01S', '*02S']:
    #            return idx


#<<<<< FORMER

#def all_events(file):
#    all_events = []
#    home_score = '00'
#    away_score = '00'
#    with open(file, 'r', encoding='utf-8') as f:
#        lines = islice(f, 73, 5000)
#        for file_ in lines:
#            line = file_.split(';')
#            skill = convert_event(file, line, home_score, away_score)
#            all_events.append(skill)
#            if skill['descrption'] == 'point':
#                home_score = skill['home_score']
#                away_score = skill['away_score']
#        return all_events