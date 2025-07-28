#DESCRIPTION:   Bash script for generating files and graphs of the power spectral density 
#               and probability density function for each seismic station.
#               This is code for XX1, XX2, XX3, XX4, XX5, XX6 and XX7 test stations.

#!/bin/bash

#STARTTIME=$(date -d '8 day ago' +'%Y-%m-%d')
#ENDTIME=$(date -d '1 day ago' +'%Y-%m-%d')

cd /home/ispaq
source /home/miniconda3/etc/profile.d/conda.sh

#conda activate ispaq

STARTTIME='2024-12-05'
ENDTIME='2024-12-19'
echo ----------- XX1 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX1.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

STARTTIME='2024-12-05'
ENDTIME='2024-12-19'
echo ----------- XX2 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX2.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

STARTTIME='2024-12-05'
ENDTIME='2024-12-19'
echo ----------- XX3 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX3.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

STARTTIME='2024-12-05'
ENDTIME='2024-12-19'
echo ----------- XX4 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX4.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

STARTTIME='2024-12-05'
ENDTIME='2024-12-13'
echo ----------- XX5 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX5.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

STARTTIME='2024-12-05'
ENDTIME='2024-12-19'
echo ----------- XX6 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX6.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

STARTTIME='2024-12-05'
ENDTIME='2024-12-19'
echo ----------- XX7 working time_period : $STARTTIME - $ENDTIME -----------
python ./run_ispaq.py -P ./preference_files/XX7.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

#conda deactivate

cd ..
