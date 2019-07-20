import os, sys, json
import mysql.connector as mysqldb

resultDir = '../data/'
data = {}

mysql_conn = mysqldb.connect(user='josh', password='diamondthth11', database='clr')
cursor = mysql_conn.cursor()

try:
    cursor.execute("""
        SELECT park_id,
            name,
            address,
            city,
            state
        FROM parks
    """)
except mysqldb.Error as err:
    print('Something went wrong: {}', format(err))
    sys.exit(1)

data['parks'] = [{'id': park[0], 'name': park[1], 'address': ', '.join(park[2:])} for park in cursor.fetchall()]

with open(os.path.join(resultDir, 'parks.json'), 'w') as file:
    json.dump(data, file, indent=1)