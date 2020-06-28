#!/bin/bash
country="ISR"
data_file="/tmp/covid-data.csv"
processed_data_file="/tmp/processed_covid_data.csv"
wget https://covid.ourworldindata.org/data/owid-covid-data.csv -O ${data_file}
head -n 1 ${data_file} > ${processed_data_file}
grep ${country} ${data_file} >> ${processed_data_file}

