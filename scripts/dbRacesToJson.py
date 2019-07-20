#!/usr/bin/env python3
import os, sys, json
import mysql.connector as mysqldb
from datetime import datetime

resultsDir = '../data/'
races_fields = ['name', 'date', 'form_url', 'park_id', 'fees']
data = {'races': []}
past_data = {'races': []}


mysql_conn = mysqldb.connect(user='josh', password='diamondthth11', database='clr')
cursor = mysql_conn.cursor()

# Get races ordered by race_date ascending
try:
    cursor.execute("""
        SELECT race_id,
            name AS race_name,
            DATE_FORMAT(datetime, '%Y-%m-%d') AS race_date,
            TIME_FORMAT(datetime, '%H:%i') AS race_time,
            form_url,
            park_id
        FROM races
        ORDER BY race_date ASC
    """)
except mysqldb.Error as err:
    print('Something went wrong: {}', format(err))
    sys.exit(1)

races = {race[0]: list(race[1:]) for race in cursor.fetchall()}

# Add fees to races
# races[key]: 0: name; 1: date (yyyy-mm-dd); 2: time 3: form_url; 4: park_id; 5: fee_array
for key in races.keys():
    try:
        cursor.execute("""
            SELECT fee,
                per,
                date_rel,
                DATE_FORMAT(due, '%%b %%e, %%Y') AS due_date
            FROM fees
            WHERE race_id = %d
        """ % key)
    except mysqldb.Error as err:
        print('Something went wrong: {}', format(err))
        sys.exit(1)
    fees = [' '.join([str(v) for v in val]) for val in cursor.fetchall()]
    races[key].append(fees)

    race_data = {}
    race_data['name'] = races[key][1][:4] + ' ' + races[key][0]
    race_data['date'] = races[key][1]
    race_data['time'] = races[key][2]
    race_data['park'] = races[key][4]
    race_data['form'] = races[key][3]
    race_data['fees'] = races[key][5]

    if datetime.strptime(race_data['date'], '%Y-%m-%d') > datetime.now():
        data['races'].append(race_data)
    else:
        past_data['races'].append(race_data)

with open(os.path.join(resultsDir,'races.json'), 'w') as file:
    json.dump(data, file, indent=1)

with open(os.path.join(resultsDir,'past_races.json'), 'w') as file:
    json.dump(past_data, file, indent=1)