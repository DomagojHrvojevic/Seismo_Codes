#DESCRIPTION:   bash script for calculating metric text .csv files (data quality info), and using
#               them to create .txt file that contains all problems which is than sent via mail.
#               This is code for XX1, XX2, XX3, XX4, XX5, XX6 and XX7 test stations.

#!/bin/bash

#when all is calculated on same date then uncomment this
#STARTTIME=$(date -d '241 day ago' +'%Y-%m-%d')
#STARTTIME="2024-11-07" #fixate on specific date

cd /home/ispaq
#source /home/miniconda3/etc/profile.d/conda.sh
#conda activate ispaq

for i in {4..18}; do

    STARTTIME=$(date -d "$i days ago" +'%Y-%m-%d')

    echo ----------- XX1 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX1.txt -M customStats -S myStations --starttime ${STARTTIME}

    echo ----------- XX2 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX2.txt -M customStats -S myStations --starttime ${STARTTIME}

    echo ----------- XX3 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX3.txt -M customStats -S myStations --starttime ${STARTTIME}

    echo ----------- XX4 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX4.txt -M customStats -S myStations --starttime ${STARTTIME}

    echo ----------- XX5 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX5.txt -M customStats -S myStations --starttime ${STARTTIME}

    echo ----------- XX6 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX6.txt -M customStats -S myStations --starttime ${STARTTIME}

    echo ----------- XX7 working on date: $STARTTIME -----------
    python ./run_ispaq.py -P ./preference_files/XX7.txt -M customStats -S myStations --starttime ${STARTTIME}

    python ./ISPAQ_Status_test.py ${STARTTIME}
    #conda deactivate

    #cd ..

done
