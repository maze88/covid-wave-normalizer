#!/usr/bin/python
import csv
import os
import subprocess
from pprint import pprint as print  # overwrite local print function

# user args
use_cached_data = True
iso_code = "ISR"
new_data_file = "data_output.csv"

# config
source_data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
raw_data_file = "/tmp/covid-data.csv"
debug = False

# converts a stringy float '3.14157' to an int 3, or an empty string to 0.
def str_to_int(s):
  if not s:
    return 0
  else:
    return int(float(s))

# main
def main():
  # check/get raw_data_file
  if use_cached_data and os.path.exists(raw_data_file):
    print("INFO: Using locally cached file '{}'!".format(raw_data_file))
  elif not use_cached_data:
    subprocess.call(["wget", source_data_url, "-O", raw_data_file])
  else:
    print("ERROR: Cannot find locally cached file '{}'!".format(raw_data_file))
    exit(2)

  # init data list
  processed_data = []

  # populate lists
  with open(raw_data_file) as csvfile:
    csv_data = csv.reader(csvfile)
    for row in csv_data:
      if row[0] == iso_code:
        new_cases = str_to_int(row[5])
        new_tests = str_to_int(row[13])
        if not new_tests:
          percent_new_cases = 0
        else:
          percent_new_cases = round(100 * new_cases/new_tests, 6)
        processed_data.append([row[3], percent_new_cases, new_cases, new_tests])
    column_names = ["date", "percent_new_cases", "new_cases", "new_tests"]

  # print data
  if debug:
    print(processed_data)

  # populate new csv file
  with open(new_data_file, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(column_names)
    for row in processed_data:
      csvwriter.writerow(row)

# boilerplate
if __name__ == "__main__":
  main()
