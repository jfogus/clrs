import os, sys, re, json
from datetime import time

resultsDir = '../supportFiles/rawResults'
for file in os.listdir(resultsDir):
    if file.endswith('.txt'):
        jsonData = {}
        with open(os.path.join(resultsDir, file), 'r') as txtFile:
            jsonData['race'] = file[11:-4].replace("Run_Walk", "Run/Walk").replace("_", " ")
            jsonData['results'] = []
            for line in txtFile:
                fields = re.split("[\s\.]{2,}", line.rstrip())
                if len(fields) == 4:
                    del fields[0]
                    result = {}
                    for (i, field) in enumerate(fields):
                        # Runner's name
                        if i == 0: result['name'] = field.title()
                        # Runner's category
                        elif i == 1:
                            parts = field.split()
                            parts[0] = "Male" if parts[0] == "M" else "Female"
                            if len(parts) == 3: parts[2] = parts[2].title()

                            result['category'] = ' '.join(parts)
                        # Runner's time (format hh:mm:ss)
                        elif i == 2:
                            parts = field.split(":")
                            if len(parts) == 2:
                                parts.insert(0, 0)
                            result['time'] = time(*[ int(x) for x in parts ]).strftime("%H:%M:%S")
                    jsonData['results'].append(result)

# TODO EVERY TIME!!! - name file yyyy_mm_dd_name_length.txt
        jsonFileName = file[:-4] + '.json'
        with open(os.path.join('../data/results', jsonFileName), 'w') as jsonFile:
            json.dump(jsonData, jsonFile, indent=4)