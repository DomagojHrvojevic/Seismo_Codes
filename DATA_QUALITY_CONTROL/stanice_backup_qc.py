###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for creating .pdf file of quality control analysis of seismological stations BACKUP data.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version:         Ubuntu-22.04
                    Python version:     3.8.19
                    pandas version:     1.5.3
                    numpy version:      1.24.4
                    fpdf version:       1.7.2
                    obspy version:      1.4.0
                    datetime version:   5.5

                    Backup station data needs to be located on standard path: /mnt/storage/podaci/{year}/{station_net}/{station}/{chanel}
                    Also, it is needed for mseed data to be in correct naming nomenclature (for example: DN.DF04..HHZ.D.2024.179)
                    Useful bash script for uppercase and formatting file names is this: /home/domagoj/uppercase.sh

                    For all stations that ispaq dinn't make PSD/PDF graphs for entire time period of available data, it is necessary to 
                    run code: /home/domagoj/DATA_QUALITY_CONTROL/stanice_backup_qc_obspy.py which will build PSD/PDF graphs with obspy 
                    and make REPORT.pdf for year in question.

    Date:           5.3.2025. - ...

    Web page:       /
"""

###########################################################PYTHON_LIBRARY###########################################################

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import obspy as ob
from fpdf import FPDF
import pandas as pd
import subprocess
import itertools
import sys
import os
from obspy import read
from obspy.io.xseed import Parser
from obspy.signal import PPSD

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#channels
channels = ['HHZ','HHN','HHE']

#set year for analysis
year = '2025'

#all paths:
stations_infile_path = '/home/domagoj/DuFAULT/STATIONS/Station_list.csv'
report_path = '/home/domagoj/DATA_QUALITY_CONTROL/REPORTS'
data_path = '/mnt/storage/podaci'
ispaq_plot_path = f'/home/domagoj/DATA_QUALITY_CONTROL/PICTURES_{year}'
PDF_PSD_path = '/home/domagoj/check_data/PDFs'

#all stations networks of stations that have backup data for qc
dir_net = os.listdir(f'{data_path}/{year}')
stations_dir = [] #empty list for stations

#get all available stations that have backup data
for i in dir_net:
    stations_dir.append(os.listdir(f'{data_path}/{year}/{i}'))

#list of all available stations backup data for setup year
stations_dir = list(itertools.chain.from_iterable(stations_dir))

#read stations_infile_path
stations = pd.read_csv(stations_infile_path)

for s in stations_dir:
    print(f'----- ANALYSIS FOR STATION {s} -----')

    #get analized_station network
    analized_station_net = stations.loc[stations['Station'] == s.upper()].iloc[0]['Network']

    #station Ston has diferent sampling_rate from the rest of the stations
    if s == 'STON':
        channel = ['BHZ','BHN','BHE']
    else:
        channel = channels
    
    #sorting all data in list according to julian date just to get STARTTIME and ENDTIME
    for c in channel[0:1]: #only one channel is enough for getting data start and end date

        lista = sorted(os.listdir(data_path + '/' + year + '/' + analized_station_net + '/' + s + '/' + f'{c}.D'))
        
        #eliminate all files that have 'mseed' in them
        lista = [x for x in lista if "mseed" not in x ]

        #getting STARTTIME
        filename = os.path.basename(lista[0])
        file_time_str = filename[-3:] + "-" + filename[-8:-4]
        file_time = datetime.strptime(file_time_str, "%j-%Y")
        STARTTIME = file_time.strftime('%Y-%m-%d')

        #getting ENDTIME
        filename = os.path.basename(lista[len(lista)-1])
        file_time_str = filename[-3:] + "-" + filename[-8:-4]
        file_time = datetime.strptime(file_time_str, "%j-%Y")
        ENDTIME = file_time.strftime('%Y-%m-%d')

    t_start = datetime.strptime(STARTTIME, "%Y-%m-%d")
    t_end = datetime.strptime(ENDTIME, "%Y-%m-%d")
    time = []

    while t_start<=t_end:
        time.append(t_start.date())
        t_start += timedelta(days=1)

    for t in time:
        print(f'----------- customStats for station: {s} on date: {t} -----------') #importatnt to make SimpleMetrics for each date
        subprocess.run(f'python /home/domagoj/ispaq/run_ispaq.py -P /home/domagoj/ispaq/preference_files/{s.upper()}.txt -M customStats -S myStations --starttime {t}', shell=True)

    print(f'----------- plot_ISPAQ for station: {s} for time interval: {STARTTIME} - {t_end.date()} -----------')
    subprocess.run(f'python /home/domagoj/DATA_QUALITY_CONTROL/plot_ISPAQ_{year}.py {STARTTIME} {t_end.date()} {s.upper()}', shell=True)

    print(f'----------- psdPdf for station: {s} for time interval: {STARTTIME} - {(t_end+timedelta(days=1)).date()} -----------')
    subprocess.run(f'python /home/domagoj/ispaq/run_ispaq.py -P /home/domagoj/ispaq/preference_files/{s.upper()}.txt -M psdPdf -S myStations --starttime {STARTTIME} --endtime {(t_end+timedelta(days=1)).date()}', shell=True)

    #deletion of vaiables that are of no use; for next station they are different 
    del STARTTIME; del ENDTIME; del t_start; del t_end

#working on pdf file report
print(f'----------- creating pdf file report for year {year} -----------')

#initializing pdf file
pdf = FPDF()

#set text font and size
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Times', 'B', size=20)

#first page of report is: weekly report and date: start - end
text_report = f"STATIONS BACKUP DATA REPORT FOR YEAR {year}"

#centering and writing text_report and text_date
page_width = pdf.w
page_height = pdf.h
text_report_width = pdf.get_string_width(text_report)

#write WEEKLY REPORT
x_position = (page_width - text_report_width) / 2
y_position = page_height / 2
pdf.text(x_position, y_position, text_report)

#insert pictures of data quality control in pdf file
for s in stations_dir:

    #get location name and network
    location = stations['Location'][stations.index[stations['Station'] == s]].iloc[0]
    network = stations['Network'][stations.index[stations['Station'] == s]].iloc[0]

    #new page for SimpleMetrics.csv plots
    pdf.add_page()
    pdf.set_font('Times', 'B', size=20)

    #station name and info
    text = s + f' - {location}'
    x_position = (page_width -  pdf.get_string_width(text)) / 2
    y_position = 8
    pdf.text(x_position, y_position, text)
    pdf.ln(5)

    #station Ston has diferent sampling_rate from the rest of the stations
    if s == 'STON':
        channel = ['BHZ','BHN','BHE']
    else:
        channel = channels

    for c in channel:
        pdf.image(ispaq_plot_path + f'/{s}{c[1:]}.png', h=pdf.h/3.5, w=pdf.w - 20)
        pdf.ln(5) #move image down by y = 5 (separate images on y axis)

        print('Plotting: ' + ispaq_plot_path + f'/{s}{c[1:]}.png')

    #new page for PDFs
    pdf.add_page()
    pdf.ln(5)
    
    for c in channel: #STON has channels BHZ, BHN, BHE and rest of them have HHZ, HHN, HHE

        lista = sorted(os.listdir(data_path + '/' + year + '/' + network + '/' + s + '/' + f'{c}.D'))
        
        #eliminate all files that have 'mseed' in them
        lista = [x for x in lista if "mseed" not in x ]

        #getting STARTTIME_1
        filename = os.path.basename(lista[0])
        file_time_str = filename[-3:] + "-" + filename[-8:-4]
        file_time = datetime.strptime(file_time_str, "%j-%Y")
        STARTTIME_1 = file_time.strftime('%Y-%m-%d')

        #getting ENDTIME_1
        filename = os.path.basename(lista[len(lista)-1])
        file_time_str = filename[-3:] + "-" + filename[-8:-4]
        file_time = datetime.strptime(file_time_str, "%j-%Y")
        ENDTIME_1 = file_time.strftime('%Y-%m-%d')

        t_start_1 = datetime.strptime(STARTTIME_1, "%Y-%m-%d")
        t_end_1 = datetime.strptime(ENDTIME_1, "%Y-%m-%d")

        print('Plotting: ' + PDF_PSD_path + f'/{network}' + f'/{s}/{network}.{s}..{c}.D.{STARTTIME_1}_{t_end_1.date()}_PDF.png')

        if not os.path.exists(PDF_PSD_path + f'/{network}' + f'/{s}/{network}.{s}..{c}.D.{STARTTIME_1}_{t_end_1.date()}_PDF.png'):
            pdf.image(f'{PDF_PSD_path}/no_PDFs/{c[1:]}_none.png',h=pdf.h/3.5, w=pdf.w - 20)
            pdf.ln(5) #move image down by y = 5 (separate images on y axis)
        else:
            pdf.image(PDF_PSD_path + f'/{network}' + f'/{s}/{network}.{s}..{c}.D.{STARTTIME_1}_{t_end_1.date()}_PDF.png', h=pdf.h/3.5, w=pdf.w - 20)
            pdf.ln(5) #move image down by y = 5 (separate images on y axis)
    
        #deletion of vaiables that are of no use; for next station they are different 
        del STARTTIME_1; del ENDTIME_1; del t_start_1; del t_end_1

pdf.output(report_path + f"/REPORT_{year}_backup_data_quality_control.pdf")
print('BACKUP STATIONS DATA REPORT IS DONE')
