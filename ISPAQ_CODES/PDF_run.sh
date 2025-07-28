#DESCRIPTION: Bash script for generating files and graphs of the power spectral density and probability density function for each seismic station.

#!/bin/bash

#STARTTIME=$(date -d '8 day ago' +'%Y-%m-%d')
#ENDTIME=$(date -d '1 day ago' +'%Y-%m-%d')

STARTTIME='2024-11-07'
ENDTIME='2024-11-10'

cd /home/ispaq
source /home/miniconda3/etc/profile.d/conda.sh

#conda activate ispaq

python ./run_ispaq.py -P ./preference_files/DF01.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
#python ./run_ispaq.py -P ./preference_files/DF02.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
#python ./run_ispaq.py -P ./preference_files/DF04.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
#python ./run_ispaq.py -P ./preference_files/DF05.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
python ./run_ispaq.py -P ./preference_files/DF06.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
python ./run_ispaq.py -P ./preference_files/STON.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
python ./run_ispaq.py -P ./preference_files/OTOC.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
python ./run_ispaq.py -P ./preference_files/VSVC.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}
python ./run_ispaq.py -P ./preference_files/ZBLJ.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

#conda deactivate

cd ..
