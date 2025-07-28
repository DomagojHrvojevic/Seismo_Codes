#DESCRIPTION:   bash script for calculating metric text .csv files (data quality info), and using
#               them to create .txt file that contains all problems which is than sent via mail.

#!/bin/bash

#when all is calculated on same date then uncomment this
#STARTTIME=$(date -d '241 day ago' +'%Y-%m-%d')
#echo DF01 working on date: $STARTTIME


cd /home/ispaq
source /home/miniconda3/etc/profile.d/conda.sh
#conda activate ispaq

#STARTTIME=$(date -d '30 day ago' +'%Y-%m-%d')
#STARTTIME="2024-11-07" #fixate on specific date
STARTTIME="2025-02-09" #fixate on specific date

#echo ----------- DF01 working on date: $STARTTIME -----------
#python ./run_ispaq.py -P ./preference_files/DF01.txt -M customStats -S myStations --starttime ${STARTTIME}

#python ./run_ispaq.py -P ./preference_files/DF02.txt -M customStats -S myStations --starttime ${STARTTIME}
#python ./run_ispaq.py -P ./preference_files/DF04.txt -M customStats -S myStations --starttime ${STARTTIME}
#python ./run_ispaq.py -P ./preference_files/DF05.txt -M customStats -S myStations --starttime ${STARTTIME}

#echo ----------- DF06 working on date: $STARTTIME -----------
#python ./run_ispaq.py -P ./preference_files/DF06.txt -M customStats -S myStations --starttime ${STARTTIME}

#echo ----------- STON working on date: $STARTTIME -----------
#python ./run_ispaq.py -P ./preference_files/STON.txt -M customStats -S myStations --starttime ${STARTTIME}

#echo ----------- OTOC working on date: $STARTTIME -----------
#python ./run_ispaq.py -P ./preference_files/OTOC.txt -M customStats -S myStations --starttime ${STARTTIME}

#echo ----------- VSVC working on date: $STARTTIME -----------
#python ./run_ispaq.py -P ./preference_files/VSVC.txt -M customStats -S myStations --starttime ${STARTTIME}

#echo ----------- ZBLJ working on date: $STARTTIME -----------
#python ./run_ispaq.py -P ./preference_files/ZBLJ.txt -M customStats -S myStations --starttime ${STARTTIME}

echo ----------- STRV working on date: $STARTTIME -----------
python ./run_ispaq.py -P ./preference_files/STRC.txt -M customStats -S myStations --starttime ${STARTTIME}

echo ----------- MRCN working on date: $STARTTIME -----------
python ./run_ispaq.py -P ./preference_files/MRCN.txt -M customStats -S myStations --starttime ${STARTTIME}

python ./ISPAQ_Status.py ${STARTTIME}
#conda deactivate

#lastly send mail with stations Error_status
#./mail.sh

cd ..
