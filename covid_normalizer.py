#!/usr/bin/python
"""
this script pulls covid data from the web and processes it, returning a csv
table with the normalized new (positive) cases compared to tests conducted.

this information allows us to better asses if/when a second wave is coming/occuring
and what is its size.

plotting the output data on a line chart in a spreadsheet is highly recommended!

note: not all countrys' data has the required fields/columns.
      israel (ISO_CODE=isr), for example, does!
"""
import csv
import os
import subprocess
import sys
from pprint import pprint as pretty_print

# config
INPUT_DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
INPUT_DATA_FILE = "/tmp/covid-data.csv"
OUTPUT_DATA_FILE = "data_output.csv"

# function definitions
def usage(exit_code=0):
    """
    prints usage instructions and help.
    """
    print("Usage: {} ISO_CODE [debug] [usecache] [help]".format(sys.argv[0]))
    print("  ISO_CODE    filter data only of this country (required).")
    print("  [debug]     script prints more output while running.")
    print("  [usecache]  use the local file (if present) instead of downloading data again.")
    print("  [help]      displays this message")
    print("Examples: {} ISR".format(sys.argv[0]))
    print("          {} isr usecache debug".format(sys.argv[0]))
    sys.exit(exit_code)

def stringy_float_to_int(stringy_float):
    """
    converts a stringy float '3.14157' to an int 3.
    if the string is empty, returns 0.
    """
    if not stringy_float:
        return 0
    return int(float(stringy_float))

def main():
    """
    downloads (if not using cache), reads and parses the covid-19 data csv
    and creates an output file with processed data.
    """
    # default arguments
    debug = False
    use_cached_data = False

    # parse arguments
    args = [arg.lower() for arg in sys.argv[1:]]
    if "help" in args:
        usage(0)
    if "debug" in args:
        debug = True
        args.remove("debug")
    if "usecache" in args:
        use_cached_data = True
        args.remove("usecache")
    if len(args) == 1:
        iso_code = args[0].upper()
    else:
        usage(1)

    # debug print config
    if debug:
        print("DEBUG: debug = {}".format(debug))
        print("DEBUG: use_cached_data = {}".format(use_cached_data))
        print("DEBUG: INPUT_DATA_FILE = {}".format(INPUT_DATA_FILE))
        print("DEBUG: INPUT_DATA_URL = {}".format(INPUT_DATA_URL))
        print("DEBUG: iso_code = {}".format(iso_code))
        print("DEBUG: OUTPUT_DATA_FILE = {}".format(OUTPUT_DATA_FILE))

    # check/get INPUT_DATA_FILE
    if use_cached_data and os.path.exists(INPUT_DATA_FILE):
        print("INFO: Using locally cached file '{}'!".format(INPUT_DATA_FILE))
    elif not use_cached_data:
        subprocess.call(["wget", INPUT_DATA_URL, "-O", INPUT_DATA_FILE])
    else:
        print("ERROR: Cannot find file '{}'!".format(INPUT_DATA_FILE))
        sys.exit(2)

    # init data list
    processed_data = []

    # populate lists
    print("INFO: reading '{}'...".format(INPUT_DATA_FILE))
    with open(INPUT_DATA_FILE) as csvfile:
        csv_data = csv.reader(csvfile)
        print("INFO: parsing csv data...")
        for row in csv_data:
            if row[0] == iso_code:
                new_cases = stringy_float_to_int(row[5])
                new_tests = stringy_float_to_int(row[13])
                if not new_tests:
                    percent_new_cases = 0
                else:
                    percent_new_cases = round(100 * new_cases/new_tests, 6)
                processed_data.append([row[3], percent_new_cases])
        column_names = ["date", "percent_new_cases"]

    # debug print data
    if debug:
        print("DEBUG: printing processed data...")
        pretty_print(processed_data)

    # populate new csv file
    print("INFO: writing to '{}'...".format(OUTPUT_DATA_FILE))
    with open(OUTPUT_DATA_FILE, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        for row in processed_data:
            csvwriter.writerow(row)

    # end
    print("Done! exiting...")

# boilerplate
if __name__ == "__main__":
    main()
