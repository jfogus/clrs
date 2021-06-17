#!/usr/bin/env python3
import os, sys, re, json

results_dir = '../supportFiles/rawResults'
for file in os.scandir(results_dir):
    root, ext = os.path.splitext(file.name)
    new_root = input("Current filename: {}\nNew filename (yyyy_mm_dd_Name_Length): ".format(root))

    if ext == '.txt':
        data = {}

        with open(file.path, 'r') as txtFile:
            # Removes the date from the filename
            data['race'] = root[11:].replace("Run_Walk", "Run/Walk").replace("_", " ")
            data['results'] = []

            for line in txtFile:
                fields = re.split("\s{2,}", line.rstrip())

                data['results'].append({
                    'name': fields[1].title(),
                    'category': fields[9].split(":")[0].replace(" - ", "-"),
                    'time': fields[6].split(".")[0]
                })

        with open(os.path.join('../data/results', new_root + '.json'), 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)