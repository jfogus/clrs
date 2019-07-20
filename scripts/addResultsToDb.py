#!/usr/bin/env python3
import os, sys, re
from datetime import time
import mysql.connector as mariadb

resultsDir = '../rawResults/'
# Parse the pdf, create txt
for file in os.listdir(resultsDir):
	records = []
	if file.endswith(".pdf"):
		# Convert the PDF to a TXT file
		pathToPDF = os.path.join(resultsDir, file)
		pathToPDF.replace(" ", "_")
		pathToTXT = os.path.splitext(pathToPDF)[0] + ".txt"
		print(pathToPDF)
		print(pathToTXT)

		# os.system("pdftotext -nopgbrk -layout " + pathToPDF + " " +	pathToTXT)
		os.system("pdftotext -layout " + pathToPDF + " " +	pathToTXT)

		# Parse the txt, create an array
		with open(pathToTXT, 'r') as txtFile:
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
							parts = field.split(':')
							if len(parts) == 2:
								parts.insert(0, 0)
							fields[i] = time(*[ int(x) for x in parts ]).strftime("%H:%M:%S")
					records.append(fields)

		# Get all races for which there are no results
		mariadb_connection = mariadb.connect(user="josh", password="diamondthth11", database="clr")
		cursor = mariadb_connection.cursor()
		try:
			cursor.execute("""
				SELECT race_id AS ID,
					name AS Name,
					DATE_FORMAT(datetime, '%Y') AS Date
				FROM races
				WHERE NOT EXISTS (
					SELECT race_id
					FROM results
					WHERE results.race_id = races.race_id
				)
			""")
		except mariadb.Error as err:
			print("Something went wrong: {}".format(err))
			sys.exit(1)
		rows = cursor.fetchall()

		# Get input on which race to input results for
		options = []
		for row in rows:
			options.append(row[0])
		print("The following races do not have results, please select one: ")
		while True:
			for row in rows:
				print("    %d - %s - (%s)" % (row[0], row[1], row[2]))
			try:
				text = int(input("Race ID: "))
			except ValueError:
				print("Not a correct input, please try again: ")
				continue

			if text in options:
				i = options.index(text)
				print(options[i])
				break
			else:
				# TODO: put this into a loop
				print("Not a correct input, please try again: ")

		# Input results
		try:
			cursor.executemany("""
				INSERT INTO results (race_id, runner, category, time)
				VALUES (%s, %s, %s, %s)
			""", ([[options[i]] + x for x in records]))
			mariadb_connection.commit()
		except mariadb.Error as err:
			print("Something went wrong: {}".format(err))
			sys.exit(1)
		cursor.close()
		mariadb_connection.close()

# os.remove(pathToPDF)
os.remove(pathToTXT)
