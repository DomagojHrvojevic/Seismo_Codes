################################################################DESCRIPTION################################################################
#!/bin/bash

#   Description:    Quality control of weekly/monthly data from active seismological stations.
#                   Using ispaq and obspy to create a pdf report from all available informations.
#                   Data quality control is made only for all ACTIVE seismological stations.
#                   RUN EVERY MONDAY AFTER MIDNIGHT.
#
#   Author:         Domagoj Hrvojevic
#   
#   Remark:         Working with miniconda ispaq environment.
#                   OS version: Ubuntu 22.04.5 LTS
#                   Python version: 3.8.19
#   
#   Date:           14.2.2025. - 26.2.2025.

################################################################DATE_START_END################################################################
STARTTIME=$(date -d '7 day ago' +'%Y-%m-%d') #7
ENDTIME=$(date -d '1 day ago' +'%Y-%m-%d') #1

echo ----------- QC for time period ${STARTTIME} - ${ENDTIME}-----------

################################################################COPY_DATA################################################################
echo ----------- copying all necessary station data files -----------

cd /home/domagoj/DATA_QUALITY_CONTROL

source /home/domagoj/miniconda3/etc/profile.d/conda.sh
conda activate ispaq

python ./grab_weekly_stations_data.py ${STARTTIME} ${ENDTIME}

cd

################################################################PSD_PDF################################################################
echo ----------- working on weekly psdPdf -----------

cd /home/domagoj/ispaq

#take last day of the week in account
ENDTIME=$(date -d '0 day ago' +'%Y-%m-%d') #0

echo ----------- psdPdf DF01 -----------
python ./run_ispaq.py -P ./preference_files/DF01.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf DF02 -----------
python ./run_ispaq.py -P ./preference_files/DF02.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf DF04 -----------
python ./run_ispaq.py -P ./preference_files/DF04.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf DF05 -----------
python ./run_ispaq.py -P ./preference_files/DF05.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf DF06 -----------
python ./run_ispaq.py -P ./preference_files/DF06.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf STON -----------
python ./run_ispaq.py -P ./preference_files/STON.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf OTOC -----------
python ./run_ispaq.py -P ./preference_files/OTOC.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf VSVC -----------
python ./run_ispaq.py -P ./preference_files/VSVC.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf ZBLJ -----------
python ./run_ispaq.py -P ./preference_files/ZBLJ.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf STRC -----------
python ./run_ispaq.py -P ./preference_files/STRC.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

echo ----------- psdPdf MRCN -----------
python ./run_ispaq.py -P ./preference_files/MRCN.txt -M psdPdf -S myStations --starttime ${STARTTIME} --endtime ${ENDTIME}

cd

################################################################PLOT_ISPAQ_AVAILABILITY################################################################
echo ----------- working on weekly PLOT_ISPAQ_AVAILABILITY -----------

#take last day of the week in account
ENDTIME=$(date -d '1 day ago' +'%Y-%m-%d') #1

cd /home/domagoj/DATA_QUALITY_CONTROL

python plot_ISPAQ_availability.py ${STARTTIME} ${ENDTIME} DF01 DF02 DF04 DF05 DF06 STON OTOC VSVC ZBLJ STRC MRCN

cd

################################################################PLOT_OBSPY_AVAILABILITY################################################################
echo ----------- working on weekly PLOT_OBSPY_AVAILABILITY -----------

cd /home/domagoj/DATA_QUALITY_CONTROL

python data_qc_obspy.py ${STARTTIME} ${ENDTIME} DF01 DF02 DF04 DF05 DF06 STON OTOC VSVC ZBLJ STRC MRCN

cd

################################################################PLOT_ISPAQ################################################################
echo ----------- working on weekly PLOT_ISPAQ -----------

#take last day of the week in account

cd /home/domagoj/DATA_QUALITY_CONTROL

python plot_ISPAQ.py ${STARTTIME} ${ENDTIME} DF01 DF02 DF04 DF05 DF06 STON OTOC VSVC ZBLJ STRC MRCN

cd

################################################################REPORT################################################################
echo ----------- working on weekly REPORT -----------

cd /home/domagoj/DATA_QUALITY_CONTROL

python data_quality_control_analysis.py ${STARTTIME} ${ENDTIME} DF01 DF02 DF04 DF05 DF06 STON OTOC VSVC ZBLJ STRC MRCN

#conda deactivate

cd
