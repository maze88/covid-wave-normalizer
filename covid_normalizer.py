#!/usr/bin/python
import csv
import os
import subprocess
from pprint import pprint as print  # overwrite local print function

# user args
debug = False
use_cached_data = True
iso_code = "ISR"
output_data_file = "data_output.csv"

# config
source_data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
raw_data_file = "/tmp/covid-data.csv"

# converts a stringy float '3.14157' to an int 3, or an empty string to 0.
def str_to_int(s):
  if not s:
    return 0
  else:
    return int(float(s))

# main
def main():
  # debug print config
  if debug:
    print("DEBUG: debug = {}".format(debug))
    print("DEBUG: use_cached_data = {}".format(use_cached_data))
    print("DEBUG: raw_data_file = {}".format(raw_data_file))
    print("DEBUG: iso_code = {}".format(iso_code))
    print("DEBUG: source_data_url = {}".format(source_data_url))
    print("DEBUG: output_data_file = {}".format(output_data_file))

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
    print("INFO: reading '{}'...".format(raw_data_file))
    csv_data = csv.reader(csvfile)
    for row in csv_data:
      if row[0] == iso_code:
        new_cases = str_to_int(row[5])
        new_tests = str_to_int(row[13])
        if not new_tests:
          percent_new_cases = 0
        else:
          percent_new_cases = round(100 * new_cases/new_tests, 6)
        processed_data.append([row[3], percent_new_cases])
    column_names = ["date", "percent_new_cases"]

  # debug print data
  if debug:
    print("DEBUG: printing processed data = ")
    print(processed_data)

  # populate new csv file
  with open(output_data_file, 'w') as csvfile:
    print("INFO: writing to '{}'...".format(output_data_file))
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(column_names)
    for row in processed_data:
      csvwriter.writerow(row)

  print("Done! exiting...")

# boilerplate
if __name__ == "__main__":
  main()
