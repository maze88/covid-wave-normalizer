#!/usr/bin/python
import csv
import subprocess

country = "ISR"
data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
data_file = "/tmp/covid-data.csv"

subprocess.call(["wget", data_url, "-O", data_file])
with open(data_file) as csvfile:
  csv_data = csv.reader(csvfile)
  for row in csv_data:
      print(', '.join(row))
