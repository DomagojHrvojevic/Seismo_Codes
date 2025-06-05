###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for generating PSD/PDF graphs with obspy for stations that haven't got one from ispaq.
                    This code needs to be runned after /home/domagoj/DATA_QUALITY_CONTROL/stanice_backup_qc.py and only 
                    for stations at years in which there is no corresponding PSD/PDF graphs.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version: Ubuntu-22.04
                    Python version:     3.8.19
                    pandas version:     1.5.3
                    obspy version:      1.4.0
                    datetime version:   5.5

    Date:           17.3.2025. - ...

    Web page:       /
"""

###########################################################PYTHON_LIBRARY###########################################################

from datetime import datetime, timedelta
import obspy as ob
import pandas as pd
from obspy.imaging.cm import pqlx
from obspy.io.xseed import Parser
from obspy.signal import PPSD
from fpdf import FPDF
import os

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

path_PSD_save_figure = '/home/domagoj/check_data/PDFs'
stations_infile_path = '/home/domagoj/DuFAULT/STATIONS/Station_list.csv'
report_path = '/home/domagoj/DATA_QUALITY_CONTROL/REPORTS'
data_path = '/mnt/storage/podaci'
PDF_PSD_path = '/home/domagoj/check_data/PDFs'

#read stations_infile_path
stations_csv = pd.read_csv(stations_infile_path)

#channels
channels = ['HHZ','HHN','HHE']

#set all years for analysis (for specific year - just leave that single year in list)
years = ['2025']#['2023', '2024', '2025'] #['2023', '2024']

#write all stations eligible for PDF/PSD graphs (edit list of stations for analysis)
stations_2023 = ['DF01', 'DF02', 'DF04', 'DF06', 'OTOC']
stations_2024 = ['DF01', 'DF02', 'DF04', 'DF06', 'MRCN', 'STRC', 'TRNV', 'VTLJ', 'OTOC']
stations_2025 = ['DF01', 'DF02', 'STRC']

for year in years:

    if year == '2023':
        stations = stations_2023
    elif year == '2024':
        stations = stations_2024
    elif year == '2025':
        stations = stations_2025

    for station in stations:

        #get station network
        station_network = stations_csv.loc[stations_csv['Station'] == station.upper()].iloc[0]['Network']

        for c in channels: #loop through all channels

            print(f'------- DRAW PDF/PSD FOR {c}_{station} - {year}-------')

            list_of_files = sorted(os.listdir(data_path + '/' + year + '/' + station_network + '/' + station + '/' + f'{c}.D'))
            
            #eliminate all files that have 'mseed' in them
            list_of_files = [x for x in list_of_files if "mseed" not in x ]

            #getting STARTTIME
            filename = os.path.basename(list_of_files[0])
            file_time_str = filename[-3:] + "-" + filename[-8:-4]
            file_time = datetime.strptime(file_time_str, "%j-%Y")
            STARTTIME = file_time.strftime('%Y-%m-%d')

            #getting ENDTIME
            filename = os.path.basename(list_of_files[len(list_of_files)-1])
            file_time_str = filename[-3:] + "-" + filename[-8:-4]
            file_time = datetime.strptime(file_time_str, "%j-%Y")
            ENDTIME = file_time.strftime('%Y-%m-%d')

            STARTTIME = datetime.strptime(STARTTIME, "%Y-%m-%d")
            ENDTIME = datetime.strptime(ENDTIME, "%Y-%m-%d")

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

            #if PSD/PDF exists it is not necessary to meke new one with obspy DN.DF04..HHN.D.2025-03-10_2025-03-16_PDF
            if not os.path.exists(f'{path_PSD_save_figure}/{station_network}/{station}/{station_network}.{station}..{c}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF.png'):

                #initialize ppsd variable
                ppsd = ''

                for file in list_of_files:
                
                    #reading MSEED data, selecting correct trace and metadata
                    st = ob.read(data_path + '/' + str(year) + '/' + station_network + '/' + station + '/' + f'{c}.D' + '/' + file)

                    #select all available traces of mseed file
                    traces = st.select(id=f"{station_network}.{station}..{c}")
                    
                    #inventory
                    inv = ob.read_inventory(f"/home/domagoj/check_data/{station}.xml")
                    
                    #counter
                    counter = 0

                    #loop through all traces
                    for trace in traces:

                        #if trace is longer than this PPSD's 'ppsd_length' (3600.0 seconds) -> add that trace
                        if trace.stats.npts > trace.stats.sampling_rate * 3600:

                            #initialize ppsd instance -> just once, only first time!!!
                            if ppsd == '':
                                ppsd = PPSD(trace.stats, metadata=inv)
                                ppsd.add(st[counter])

                            #add trace to existing ppsd
                            else:
                                #add data for that exact trace
                                ppsd.add(st[counter])

                            #print information for tracking progress (added trace)
                            print(f'ADDED TO PPSD: {st[counter]}')
                        
                        else:
                            #print information for tracking progress (dismissed trace)
                            print(f'NOT ADDED TO PPSD: {st[counter]}')

                        counter += 1

                ppsd.plot(f'{path_PSD_save_figure}/{station_network}/{station}/{station_network}.{station}..{c}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF.png', cmap=pqlx)
                print(f'DONE - {station_network}.{station}..{c}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF')
            
            else:
                print(f'FILE EXISTS {path_PSD_save_figure}/{station_network}/{station}/{station_network}.{station}..{c}.D.{STARTTIME.year}-{start_month}-{start_day}_{ENDTIME.year}-{end_month}-{end_day}_PDF.png')

            #deletion of vaiables that are of no use; for next station they are different 
            del STARTTIME; del ENDTIME
            
    #working on pdf file report
    print(f'----------- creating pdf file report for year {year} -----------')

    #path for ispaq pictures
    ispaq_plot_path = f'/home/domagoj/DATA_QUALITY_CONTROL/PICTURES_{year}'

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
    for s in stations:

        #get location name and network
        location = stations_csv['Location'][stations_csv.index[stations_csv['Station'] == s]].iloc[0]
        network = stations_csv['Network'][stations_csv.index[stations_csv['Station'] == s]].iloc[0]

        #new page for SimpleMetrics.csv plots
        pdf.add_page()
        pdf.set_font('Times', 'B', size=20)

        #station name and info
        text = s + f' - {location}'
        x_position = (page_width -  pdf.get_string_width(text)) / 2
        y_position = 8
        pdf.text(x_position, y_position, text)
        pdf.ln(5)

        for c in channels:
            pdf.image(ispaq_plot_path + f'/{s}{c[1:]}.png', h=pdf.h/3.5, w=pdf.w - 20)
            pdf.ln(5) #move image down by y = 5 (separate images on y axis)

        #new page for PDFs
        pdf.add_page()
        pdf.ln(5)
        
        for c in channels: #STON has channels BHZ, BHN, BHE and rest of them have HHZ, HHN, HHE

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
    print(f'BACKUP STATIONS DATA REPORT IS DONE FOR YEAR {year}')
