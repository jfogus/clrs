#!/usr/bin/env python3
import os, json
from datetime import datetime

dataDir = '../data/'
newFile = os.path.join(dataDir, 'races.json')
pastFile = os.path.join(dataDir, 'past_races.json')
indexesToMove = []
dataToMove = []
data = []


def saveData(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=1)


# Pops races that have passed from races.json
with open(newFile, 'r') as file:
    data = json.load(file)

    for i, race in enumerate(data['races']):
        if datetime.strptime(race['date'], '%Y-%m-%d') <= datetime.today():
            indexesToMove.append(i)

for i in indexesToMove:
    dataToMove.append(data['races'].pop(i))

saveData(newFile, data)

# Adds past races to past_races.json
with open(pastFile, 'r') as file:
    data = json.load(file)
    data['races'].extend(dataToMove)

saveData(pastFile, data)
