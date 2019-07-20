#!/usr/bin/env python3
import os, sys, json
import mysql.connector as mysqldb

resultsDir = '../data/results/'
result_fields = ['name', 'category', 'time']
data = {}

mysql_conn = mysqldb.connect(user='josh', password='diamondthth11', database='clr')
cursor = mysql_conn.cursor()

try:
    cursor.execute("""
        SELECT race_id,
            name AS race_name,
            DATE_FORMAT(datetime, '%Y_%m_%d') AS race_date
        FROM races;
    """)
except mysqldb.Error as err:
    print('Something went wrong: {}',format(err))
    sys.exit(1)

# race: 0: race_id, 1: race_name, 2: race_date (yyyy_mm_dd)
races = {race[0]: [race[2],race[1]] for race in cursor.fetchall()}

for key in races.keys():
    try:
        cursor.execute("""
            SELECT runner,
                category,
                TIME_FORMAT(time, '%%H:%%i:%%s')
            FROM results
            WHERE race_id = %d
            ORDER BY time ASC
        """ % key)
    except mysqldb.Error as err:
        print('Something went wrong: {}', format(err))
        sys.exit(1)
    
    races[key].append(cursor.fetchall())

# races[key]: 0: race_date (yyyy_mm_dd), 1: race_name, 2: results_array [0: name, 1: category, 2: time] (ordered by time ASC)
for i, race in races.items():
    if len(race[2]) == 0: continue
        
    fileName = os.path.join(resultsDir, race[0] + '_' + race[1].replace(' ', '_').replace('/', '_') + '.json')

    data['race'] = race[0][:4] + ' ' + race[1]
    data['results'] = []

    for j, result in enumerate(race[2]):
        data['results'].append(dict(zip(result_fields,result)))

    with open(fileName, 'w') as file:
        json.dump(data, file, indent=1)
