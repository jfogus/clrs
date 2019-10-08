# TODO: Take pdf from rawResults folder, make into JSON, update races/past_races with moveOldRaces.py
# TODO: DON'T USE, THIS DOES NOT WORK!!!
import os, sys, re

resultsDir = '../supportFiles/rawResults'
for file in os.listdir(resultsDir):
    if file.endswith('.txt'):
        with open(file, 'r') as txtFile:
            for line in txtFile:
                fields = re.split("[\s\.]{2,}", line.rstrip())
                if len(fields) == 4:
                    del fields[0]
                    for (i, field) in enumerate(fields):
                        # Runner's name
                        if i == 0: fields[i] = field.title()
                        # Runner's category
                        elif i == 1:
                            parts = field.split()
                            parts[0] = "Male" if parts[0] == "M" else "Female"
                            if len(parts) == 3: parts[2] = parts[2].title()

                            fields[i] = ' '.join(parts)
                        # Runner's time (format hh:mm:ss)
                        elif i == 2:
                            parts = field.split(":")
                            if len(parts) == 2:
                                parts.insert(0, 0)
                            fields[i] = time(*[ int(x) for x in parts ]).strftime("%H:%M:%S")
