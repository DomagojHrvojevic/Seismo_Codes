#DESCRIPTION:   bash script for calculating metric text .csv files (data quality info), and using
#               them to create .txt file that contains all problems which is than sent via mail.

#!/bin/bash

STARTTIME=$(date -d '1 day ago' +'%Y-%m-%d')

cd /home/ispaq
source /home/anaconda3/etc/profile.d/conda.sh
conda activate ispaq
python ./run_ispaq.py -P ./preference_files/DF01.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/DF02.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/DF04.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/DF05.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/DF06.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/STON.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/OTOC.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/VSVC.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/ZBLJ.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/STRC.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./run_ispaq.py -P ./preference_files/MRCN.txt -M customStats -S myStations --starttime ${STARTTIME}
python ./ISPAQ_Status.py ${STARTTIME}
conda deactivate
cd ..