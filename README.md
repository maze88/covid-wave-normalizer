# CoViD-19 wave normalizer

## What it does

This script pulls CoViD-19 data from the web and processes it, returning a csv
table with the daily new cases, normalized to the daily tests conducted.
In simple terms that is: percent positive tests, per day.

## Why to use it

This information allows us to better asses the presence and magnitude of a second CoViD-19 wave.

## How to use it

From your command line: `./covid_normalizer.py ISO_CODE [debug] [usecache] [help]`, output data will be save to `data_output.csv` in the current working directory.

Where:
- `ISO_CODE` (required) filter data only of this country.
- `debug`    script prints more output while running.
- `usecache` use the local file (if present) instead of downloading data again.
- `help`     displays usage instructions.

Examples:
- `./covid_normalizer.py ISR`
- `./covid_normalizer.py isr usecache debug`

## What to do with output

- Plotting the output data on a chart in a spreadsheet is highly recommended!
- Besides that, arguing on the internet with conspiracy theorists and anti-vaxxers *might* be fun...

### Note:

Not all countrys' data has the required columns to perform this calculation.
ISO codes USA and ISR, for example, do!
