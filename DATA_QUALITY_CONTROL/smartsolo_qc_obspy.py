###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for creating quality control analysis .pdf file of SmartSolo seismological stations data.
                    IGU-BD3C-5 instrument is Broadband Integrated 3 Component Seismograph. For more info check web page.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version:         Ubuntu-22.04
                    Python version:     3.8.19
                    pandas version:     1.5.3
                    numpy version:      1.24.4
                    fpdf version:       1.7.2
                    obspy version:      1.4.0
                    datetime version:   5.5

    Date:           7.4.2025. - ...

    Web page:       https://smartsolo.com/igu-bd3c-5.html
"""

###########################################################PYTHON_LIBRARY###########################################################

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import obspy as ob
from fpdf import FPDF
import pandas as pd
import subprocess
import os
from obspy import read
from obspy.io.xseed import Parser
from obspy.imaging.cm import pqlx
from obspy.signal import PPSD
import gc

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#paths:
PSD_save_figure_path = '/home/domagoj/check_data/PDFs'
data_availability_save_path = '/home/domagoj/DATA_QUALITY_CONTROL/PICTURES'
stations_infile_path = '/mnt/smartsolo_data/smartsolo_stations.txt'
save_report_path = '/home/domagoj/DATA_QUALITY_CONTROL/REPORTS'
data_path_static = '/mnt/smartsolo_data'

#read stations_infile_path
stations_csv = pd.read_csv(stations_infile_path)

#channels
channels = ['HHZ','HHN','HHE']

#loop through all smartsolo stations
for i_d in stations_csv['ID']:
    
    #necessary informations for data analysis
    station_net = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['network']
    station = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['Kod_postaje']
    location_name = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['names']
    activity_period = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['period_aktivnosti']

    #new data path depending on where data is stored:
    if station_net == 'PK':
        data_path_dynamic = data_path_static + f'/Paklenica-NET/{location_name}/{i_d}'
    elif station_net == 'HR':
        data_path_dynamic = data_path_static + f'/DuFAULT/{location_name}/{i_d}'

    #all files in data folder
    mseed_files = os.listdir(data_path_dynamic)

    #extract only miniseed data files (smartsolo instrument writes seismo data in MiniSeed format):
    mseed_files = [i for i in mseed_files if 'MiniSeed' in i]

    #smartsolo files grouped by components and sorted by name (equivalent to time):
    smartsolo_files_z = sorted([i for i in mseed_files if 'Z' in i])
    smartsolo_files_x = sorted([i for i in mseed_files if 'X' in i])
    smartsolo_files_y = sorted([i for i in mseed_files if 'Y' in i])
    smartsolo_files = [smartsolo_files_z,smartsolo_files_x,smartsolo_files_y]
    
    #loop through list of lists of mseed data by components
    for coun,mseed_files_by_components in enumerate(smartsolo_files):

        #print info for user to know which step of data formatting is being processed
        print(f'Working on station: {station}, network: {station_net}, component: {channels[coun]}')

        #loop list of mseed files of one component
        for count,mseed_file in enumerate(mseed_files_by_components):
            
            #reed all mseed files together for each component separately
            if count == 0:
                file = ob.read(data_path_dynamic + f'/{mseed_file}')
            else:
                file += ob.read(data_path_dynamic + f'/{mseed_file}')

        """ ####THIS IS KILLING PROGRAM EXECUTION BECAUSE MERGING IS HEAVY ON RAM -> NO NEED FOR THAT#### 
            #merge traces of all smartsolo mseed files of one component and fill gaps with zeroes
            if len(file) > 1:
                file.merge(method=0, fill_value=None)
            if isinstance(file[0].data, np.ma.masked_array):
                file[0].data = file[0].data.filled()
        """

        #standard naming of stats in all traces
        for stat in file:
            #renaming stats parameters
            stat.stats['station'] = station
            stat.stats['network'] = station_net
            stat.stats['location'] = ''
            stat.stats['channel'] = channels[coun]

        #extract sampling_rate
        sampling_rate = file[0].stats.sampling_rate

        #getting STARTTIME and ENDTIME
        file_time = datetime.strptime(activity_period.split('-')[0], "%d.%m.%Y")
        STARTTIME = file_time.strftime('%Y-%m-%d')
        file_time = datetime.strptime(activity_period.split('-')[1], "%d.%m.%Y")
        ENDTIME = file_time.strftime('%Y-%m-%d')
        STARTTIME = datetime.strptime(STARTTIME, "%Y-%m-%d")
        ENDTIME = datetime.strptime(ENDTIME, "%Y-%m-%d")

        print(f'------- DRAW PDF/PSD FOR {station}_{station_net}_{channels[coun]}: {STARTTIME} - {ENDTIME} -------')

        #empty time/string variables
        start_month = ''; start_day = ''; end_month = ''; end_day = ''

        #just for naming purposes; for example: 01, 02, 03, ... 10, 11, 12
        if STARTTIME.month < 10:
            start_month = f'0{STARTTIME.month}'
        else:
            start_month = f'{STARTTIME.month}'

        if STARTTIME.day < 10:
            start_day = f'0{STARTTIME.day}'
        else:
            start_day = f'{STARTTIME.day}'

        if ENDTIME.month < 10:
            end_month = f'0{ENDTIME.month}'
        else:
            end_month = f'{ENDTIME.month}'

        if ENDTIME.day < 10:
            end_day = f'0{ENDTIME.day}'
        else:
            end_day = f'{ENDTIME.day}'

        #if PSD/PDF exists it is not necessary to meke new one with obspy (naming example: DN.DF04..HHN.D.2025-03-10_2025-03-16_PDF)
        if not os.path.exists(f'{PSD_save_figure_path}/{station_net}/{station}/{station_net}.{station}..{channels[coun]}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF.png'):

            #initialize ppsd variable
            ppsd = None

            #select all available traces of mseed file
            traces = file.select(id=f"{station_net}.{station}..{channels[coun]}")
            
            #inventory
            inv = ob.read_inventory(f"/home/domagoj/check_data/{station}.xml")

            #loop through all traces
            for counter,trace in enumerate(traces):

                #if trace is longer than this PPSD's 'ppsd_length' (3600.0 seconds = 1 hour) -> add that trace
                if trace.stats.npts > trace.stats.sampling_rate * 3600:

                    #initialize ppsd instance -> just once, only first time!!!
                    if ppsd is None:
                        ppsd = PPSD(trace.stats, metadata=inv)
                        ppsd.add(file[counter]) #add trace

                    #else, add trace to existing ppsd
                    else:
                        #add data for that exact trace
                        ppsd.add(file[counter])

                    #print information for tracking progress (added trace)
                    print(f'ADDED TO PPSD: {file[counter]}')
                
                else:
                    #print information for tracking progress (dismissed trace)
                    print(f'NOT ADDED TO PPSD: {file[counter]}')
                
                

            ppsd.plot(f'{PSD_save_figure_path}/{station_net}/{station}/{station_net}.{station}..{channels[coun]}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF.png', cmap=pqlx)
            print(f'DONE - {station_net}.{station}..{channels[coun]}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF')

        else:
            print(f'FILE EXISTS {PSD_save_figure_path}/{station_net}/{station}/{station_net}.{station}..{channels[coun]}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF.png')

        #garbage collection and deletion of vaiables that are of no use; for next station they are different 
        del STARTTIME; del ENDTIME; del file
        gc.collect()

    #draw obspy data availability of smartsolo data 
    print(f'------- DRAW OBSPY DATA AVAILABILITY FOR {station}_{station_net}_{channels[0]}_{channels[1]}_{channels[2]} -------')

    #empty string for storing full data paths of each smartsolo file
    filepaths = ''
    for i in smartsolo_files:
        for j in i:
            filepaths += f'{data_path_dynamic}/{j} '
    
    #make obspy data accessibility plot
    scp_result = subprocess.run(f"obspy-scan {filepaths}-o {data_availability_save_path}/{station}.png", shell=True)

    #garbage collection and deletion of vaiables that are of no use; for next station they are different 
    del scp_result
    gc.collect()

#working on pdf file report
print(f'------- creating pdf file report for smartsolo data -------')

#initializing pdf file
pdf = FPDF()

#set text font and size
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Times', 'B', size=20)

#first page of report is: weekly report and date: start - end
text_report = f"SMARTSOLO STATIONS DATA REPORT"

#centering and writing text_report and text_date
page_width = pdf.w
page_height = pdf.h
text_report_width = pdf.get_string_width(text_report)

#write WEEKLY REPORT
x_position = (page_width - text_report_width) / 2
y_position = page_height / 2
pdf.text(x_position, y_position, text_report)

#loop through all smartsolo stations
for i_d in stations_csv['ID']:

    #necessary informations for data analysis
    station_net = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['network']
    station = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['Kod_postaje']
    location_name = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['names']
    activity_period = stations_csv.loc[stations_csv['ID'] == i_d].iloc[0]['period_aktivnosti']

    #new page for SimpleMetrics.csv plots
    pdf.add_page()
    pdf.set_font('Times', 'B', size=20)

    #station name and info
    text = f'{station} - {station_net} - {location_name} - {activity_period}'
    x_position = (page_width -  pdf.get_string_width(text)) / 2
    y_position = 8
    pdf.text(x_position, y_position, text)
    pdf.ln(page_height/3)

    #name of the graph
    pdf.set_font('Times', size=15)
    title_text = 'Data availability in instruments monitoring period'
    title_text_width = pdf.get_string_width(title_text)
    x_position = (page_width - title_text_width) / 2
    y_position = page_height / 2.8
    pdf.text(x_position, y_position, 'Data availability in monitoring period')

    #data availability graph
    pdf.image(f'{data_availability_save_path}/{station}.png', h=pdf.h/3.5, w=pdf.w - 20)

    #new page for PDFs
    pdf.add_page()
    pdf.ln(5)
    
    #loop through all channels for inserting psd graphs
    for c in channels:

        #getting STARTTIME_1
        file_time = datetime.strptime(activity_period.split('-')[0], "%d.%m.%Y")
        STARTTIME_1 = file_time.strftime('%Y-%m-%d')

        #getting ENDTIME_1

        file_time = datetime.strptime(activity_period.split('-')[1], "%d.%m.%Y")
        ENDTIME_1 = file_time.strftime('%Y-%m-%d')

        t_start_1 = datetime.strptime(STARTTIME_1, "%Y-%m-%d")
        t_end_1 = datetime.strptime(ENDTIME_1, "%Y-%m-%d")

        print('Plotting in pdf file: ' + PSD_save_figure_path + f'/{station_net}' + f'/{station}/{station_net}.{station}..{c}.D.{STARTTIME_1}_{t_end_1.date()}_PDF.png')

        if not os.path.exists(PSD_save_figure_path + f'/{station_net}' + f'/{station}/{station_net}.{station}..{c}.D.{STARTTIME_1}_{t_end_1.date()}_PDF.png'):
            pdf.image(f'{PSD_save_figure_path}/no_PDFs/{c[1:]}_none.png',h=pdf.h/3.5, w=pdf.w - 20)
            pdf.ln(5) #move image down by y = 5 (separate images on y axis)
        else:
            pdf.image(PSD_save_figure_path + f'/{station_net}' + f'/{station}/{station_net}.{station}..{c}.D.{STARTTIME_1}_{t_end_1.date()}_PDF.png', h=pdf.h/3.5, w=pdf.w - 20)
            pdf.ln(5) #move image down by y = 5 (separate images on y axis)
    
        #garbage collection and deletion of vaiables that are of no use; for next station they are different 
        del STARTTIME_1; del ENDTIME_1; del t_start_1; del t_end_1
        gc.collect()

pdf.output(save_report_path + f"/SMARTSOLO_REPORT_data_quality_control.pdf")
print('SMARTSOLO STATIONS DATA REPORT IS DONE')
