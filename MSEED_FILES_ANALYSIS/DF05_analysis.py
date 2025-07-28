###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for analysis of DF05 station.
                    This code can be used for other stations.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version:         Ubuntu-22.04
                    Python version:     3.8.19
                    pandas version:     1.5.3
                    datetime version:   5.5
                    obspy version:      1.4.0
                    numpy version:      1.24.4

                    This code has been made from multiple existing scripts:
                        /home/DuFAULT/DATA/copy_data.py
                        /home/DuFAULT/DATA/data_modules.py
                        /home/DuFAULT/DATA/Files.py
                        /home/MSEED_files_analysis/reading_seed_files.py

    Date:           26.2.2025. - ....
"""

###########################################################PYTHON_LIBRARY###########################################################

import sys
import os, os.path, glob, time
from datetime import datetime, timedelta
import pandas as pd
import subprocess
import data_modules as dm
from obspy import read
from obspy.io.xseed import Parser
from obspy.signal import PPSD
import shutil
import matplotlib.pyplot as plt
import obspy as ob
import numpy as np
import gc
from fpdf import FPDF

###########################################################PYTHON_FUNCTIONS###########################################################

def check_remote_directory(path):
    
    """
    Check if a remote directory exists and is accessible
    """
    
    command = f"sshpass -p '{remote_password}' ssh -p {remote_port} {remote_user}@{remote_host} 'if [ -d {path} ]; then echo exists; else echo does_not_exist; fi'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return "exists" in result.stdout.strip()

def list_remote_files(path):

    """
    List remote files in directory
    """
    
    command = f"sshpass -p '{remote_password}' ssh -p {remote_port} {remote_user}@{remote_host} 'ls {path}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.splitlines()
    else:
        print(f"Failed to list files in {path}: {result.stderr}")
        return []

def test_time_ticks(sample_rate,x,y):

    """
    Function for testing length of time ticks (if len(time_ticks) != 25)
    """

    difference = sample_rate*60*60*24 - len(x) #frequency * time - len(x) -> total time steps that have no data
    full_array = np.empty(int(len(x)+difference + 1)) * np.nan #full_array has correct dimensions for plotting ground motion activity (for time steps with no data -> none is added)
    full_array[:y.size] = y #full_array set first existing values of ground motion
    y = full_array #assign full_array to y
    x =  np.arange(0, len(full_array),1) #setting size valid total time steps (time (s) * frequency (Hz))
    time_ticks=np.arange(0,len(x),sample_rate*60*60) #setting correct time_ticks so it can be hourly displayed
    return x,y,time_ticks

###########################################################PYTHON_CODE###########################################################

#start and end date
t_start = datetime.strptime('2025-02-17', "%Y-%m-%d").date()
t_end = datetime.strptime('2025-02-23', "%Y-%m-%d").date()

#analized station data
analized_station = 'DF05'

#read stations .csv file
stations_infile_path = "/home/DuFAULT/STATIONS/Station_list.csv"
stations = pd.read_csv(stations_infile_path)
#get analized_station network
analized_station_net = stations.loc[stations['Station'] == analized_station].iloc[0]['Network']

#channels
channels = ['HHZ','HHN','HHE']
#list of dates
time = []
time_count = t_start

#add all dates in list
while time_count<=t_end:
    time.append(time_count)
    time_count += timedelta(days=1)

#remote SSH connection details
remote_host = "xxx.xx.xx.xx"
remote_user = "user"
remote_password = "password"
remote_port = 22
remote_data_folder = "/mnt/storage/podaci"

#output folders
out_folder= "/mnt/storage/podaci"
out_folder_tmp = "/mnt/storage/podaci/tmp"
out_SANDI_path = "/mnt/SANDI_PODACI"
#daily data path:
daily_data_path = '/mnt/storage/podaci'
#hourly data path:
hourly_data_path = '/mnt/SANDI_PODACI'
#pictures path:
picture_path = '/home/MSEED_files_analysis/pictures'

###########################################################DATA_TRANSFER_DAILY###########################################################

#copy data from SSH server locally
for t in time:

    print(f'------- COPY DATA FROM SSH SERVER LOCALLY - {t}-------')

    #temporary variables
    julian = ''

    #search for simpleMetrics.csv files -> transfer them locally
    try:
        infile = '/home/check_data/csv/' + analized_station + '/customStats_myStations_' + t.strftime("%Y-%m-%d") + '_simpleMetrics.csv'
        outfile = '/home/check_data/csv/' + analized_station + '/customStats_myStations_' + t.strftime("%Y-%m-%d") + '_simpleMetrics.csv'
        if not os.path.exists('/home/check_data/csv/' + analized_station):
            os.makedirs('/home/check_data/csv/' + analized_station) #create folder if it doesn't exist

        scp_command = f"sshpass -p '{remote_password}' scp -P {remote_port} {remote_user}@{remote_host}:{infile} {outfile}"
        scp_result = subprocess.run(scp_command, shell=True)

        if scp_result.returncode == 0:
            print(f"Copied {infile}")
        else:
            print(f"Failed to copy {infile}: {scp_result.stderr}")

    except Exception as e:
        print(f"Error processing file")
        continue

    #search and find .mseed files that are needed -> transfer them locally
    try:
        #input folder
        remote_in_folder = f"{remote_data_folder}/{t.year}/{analized_station_net}/{analized_station}"

        #output folder
        local_out_folder1 = os.path.join(out_folder, str(t.year), analized_station_net, analized_station)

        if check_remote_directory(remote_in_folder):
            print(f"Processing folder: {remote_in_folder}")
            
            folders_comp = list_remote_files(remote_in_folder)
            
            for folder_comp in folders_comp:
                remote_folder_comp = os.path.join(remote_in_folder, folder_comp)
                local_out_folder2 = os.path.join(local_out_folder1, folder_comp)

                if check_remote_directory(remote_folder_comp):
                    #create the local folder only if the remote folder exists
                    if not os.path.exists(local_out_folder2):
                        os.makedirs(local_out_folder2)
                        print(f"Created local directory {local_out_folder2}")
                    
                    remote_files = list_remote_files(remote_folder_comp)
                    for remote_file in remote_files:
                        try:
                            #extract file name and convert to appropriate date for filtering
                            filename = os.path.basename(remote_file)
                            file_time_str = filename[-3:] + "-" + filename[-8:-4]
                            file_time = datetime.strptime(file_time_str, "%j-%Y")

                            #copy file using SCP
                            if file_time.strftime("%d-%m-%Y") == t.strftime("%d-%m-%Y"):
                                julian = filename[-8:-4] + '.' + filename[-3:] #save ending of file (used in drawing)

                                remote_file_path = os.path.join(remote_folder_comp, filename)
                                local_file_path = os.path.join(local_out_folder2, filename)
                                
                                #save to /mnt/d/storage/podaci
                                scp_command = f"sshpass -p '{remote_password}' scp -P {remote_port} {remote_user}@{remote_host}:{remote_file_path} {local_file_path}"
                                scp_result = subprocess.run(scp_command, shell=True)
                                
                                #save to /mnt/d/storage/podaci/tmp
                                if not os.path.exists(f"{out_folder_tmp}/{analized_station_net}/{analized_station}/{folder_comp}"):
                                    os.makedirs(f"{out_folder_tmp}/{analized_station_net}/{analized_station}/{folder_comp}")

                                scp_command = f"sshpass -p '{remote_password}' scp -P {remote_port} {remote_user}@{remote_host}:{remote_file_path} {out_folder_tmp}/{analized_station_net}/{analized_station}/{folder_comp}"
                                scp_result = subprocess.run(scp_command, shell=True)
                                
                                if scp_result.returncode == 0:
                                    print(f"Copied {filename}")
                                else:
                                    print(f"Failed to copy {filename}: {scp_result.stderr}")

                        except Exception as e:
                            print(f"Error processing file {remote_file}: {e}")
                            continue
                else:
                    print(f"Remote subdirectory {remote_folder_comp} does not exist, skipping.")

        else:
            print(f"Remote directory {remote_in_folder} does not exist, skipping.")
                
    except Exception as e:
        print(f"Error processing station {analized_station}: {e}")
        continue

    ###########################################################SANDI_DATA_HOURLY###########################################################
    
    print(f'------- FORMAT HOURLY DATA - {t}-------')

    # Read station info -> extract only info for analized station in sta_dict
    stations_infile = "/home/DuFAULT/DATA/Station_list.csv"
    sta_dict = dm.read_network(stations_infile)
    for i in sta_dict:
        if sta_dict[i]['Station'] == analized_station:
            sta_dict = sta_dict[i]
            break

    # Input data folder
    data_folder = '/mnt/storage/podaci/tmp'

    # Output folder
    out_folder = '/mnt/SANDI_PODACI'

    # List of components <class 'str'> 26-02-2025
    date = t
    components = ['z','n','e']

    stla = sta_dict['Latitude']
    stlo = sta_dict['Longitude']
    stel = sta_dict['Elevation']
    stnm = sta_dict['Station'] 
    snet = sta_dict['Network']

    for comp in components:
        # Run the module that formats and saves the data
        try:
            dm.get_files(data_folder=data_folder, out_folder=out_folder,\
            stla=stla, stlo=stlo, stel=stel, stnm=stnm, snet=snet, comp=comp, conv_time=f'{date.day}-{date.month}-{date.year}')
        except Exception as e:
            print(e)

    #remove temporary files that are stored just to format hourly data
    shutil.rmtree(out_folder_tmp)
    
    ###########################################################CALCULATING_DAILY_SEISMOGRAMS###########################################################

    print(f'------- DRAW DAILY SEISMOGRAMS - {t}-------')

    #for plotting daily data
    fig, ax = plt.subplots(3,1,figsize=(30, 20))

    for i in channels: #loop through all channels

        #reading MSEED files
        st = ob.read(daily_data_path + '/' + str(t.year) + '/' + analized_station_net + '/' + analized_station + '/' + f'{i}.D' + '/' + f'{analized_station_net}.{analized_station}..{i}.D.{julian}')

        #print(st[0].stats) #printing stats of input file

        #get sample_rate and dataquality
        sample_rate = st[0].stats.sampling_rate #get sample rate in Hz

        #The actual data is stored as a ndarray in the data attribute of each trace.
        #print(st[0].data)
        y = st[0].data
        x = np.arange(0,len(y),1)

        #Write data back to disc or a file like object
        #st.write('Mini-SEED-filename.mseed', format='MSEED') 

        #time_ticks=np.arange(0,len(x),sample_rate*60*60)
        #if len(time_ticks) != 25: #if data quantity is lower that it should be for 24 hours
        #    x,y,time_ticks = test_time_ticks(sample_rate,x,y) #set no data to np.nan

        #plot mseed seismic activity data on y-axis and time on x-axis
        plt.suptitle(f'{analized_station_net}_{analized_station}_{i}_{t}', fontsize=30)
        ax[channels.index(i)].set_xlabel ('Time (h)', fontsize=25)
        ax[channels.index(i)].set_ylabel (f'{i} (count)', fontsize=25)
        ax[channels.index(i)].plot(x,y)
        #ax[channels.index(i)].set_xticks(time_ticks) #x_axis in hours
        #ax[channels.index(i)].set_xticklabels(np.arange(0,25,1), fontsize=25)
        
        #ax[channels.index(i)].set_xlim(0,sample_rate*60*60*24) # sample_rate*minutessample_rate*60*60*24
        ax[channels.index(i)].tick_params(axis='y', labelsize=25)
        ax[channels.index(i)].grid()

        #garbage collection and deletition of obspy variable to save memory
        del st
        gc.collect()

    plt.savefig(f'{picture_path}/{analized_station_net}_{analized_station}_{t.day}_{t.month}_{t.year}_daily_data.png')
    plt.close(fig) #close figure to save memory
    print(f'DONE - {analized_station_net}_{analized_station}_{t.day}_{t.month}_{t.year}_daily_data')

    ###########################################################CALCULATING_DAILY_PDF/PSD###########################################################

    print(f'------- DRAW DAILY PDF/PSD - {t}-------')

    for i in channels: #loop through all channels
        
        #reading MSEED data, selecting correct trace and metadata
        st = ob.read(daily_data_path + '/' + str(t.year) + '/' + analized_station_net + '/' + analized_station + '/' + f'{i}.D' + '/' + f'{analized_station_net}.{analized_station}..{i}.D.{julian}')

        #if trace is empty for analized_station, use digitizer default naming 6062 -> else use analized_station
        if '0 Trace(s) in Stream:' in str(st.select(id=f"{analized_station_net}.{analized_station}..{i}")):
            tr = st.select(id=f".6062..{i}".upper())[0]
            continue
        else:
            tr = st.select(id=f"{analized_station_net}.{analized_station}..{i}")[0]

        inv = ob.read_inventory(f"/home/check_data/{analized_station}.xml")

        #initialize ppsd instance
        ppsd = PPSD(tr.stats, metadata=inv)
        ppsd.add(st) #add data

        ppsd.plot(f'{picture_path}/{analized_station_net}_{analized_station}_{i}_{t.day}_{t.month}_{t.year}_daily_psd.png')
        print(f'DONE - {analized_station_net}_{analized_station}_{i}_{t.day}_{t.month}_{t.year}_daily_psd')

###########################################################MAKE_PDF_DAILY_REPORT###########################################################

print(f'------- MAKE DAILY PDF REPORT -------')

#initializing pdf file
pdf = FPDF()

#set text font and size
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Times', 'B', size=20)

#first page of report is: weekly report and date: start - end
text_report = f"{analized_station} DAILY REPORT"
text_date = f"DATE: {t_start.day}.{t_start.month}.{t_start.year} - {t_end.day}.{t_end.month}.{t_end.year}"

#centering and writing text_report and text_date
page_width = pdf.w
page_height = pdf.h
text_report_width = pdf.get_string_width(text_report)
text_date_width = pdf.get_string_width(text_date)

#write WEEKLY REPORT
x_position = (page_width - text_report_width) / 2
y_position = page_height / 2
pdf.text(x_position, y_position, text_report)

#write date span
x_position = (page_width - text_date_width) / 2
y_position += 10
pdf.text(x_position, y_position, text_date)


for t in time:
    pdf.add_page()
    pdf.image(f'{picture_path}/{analized_station_net}_{analized_station}_{t.day}_{t.month}_{t.year}_daily_data.png', h=pdf.h/4.1, w=pdf.w - 20)
    pdf.ln(-6) #move image up (separate images on y axis)

    for c in channels: #STON has channels BHZ, BHN, BHE and rest of them have HHZ, HHN, HHE; if file exists plot it, if not than don't plot it
        if os.path.isfile(f'{picture_path}/{analized_station_net}_{analized_station}_{c}_{t.day}_{t.month}_{t.year}_daily_psd.png'):
            pdf.image(f'{picture_path}/{analized_station_net}_{analized_station}_{c}_{t.day}_{t.month}_{t.year}_daily_psd.png', h=pdf.h/4.1, w=pdf.w - 20)
        else:
            continue
        pdf.ln(-6) #move image up (separate images on y axis)

pdf.output(f'/home/MSEED_files_analysis/reports/{analized_station}_DAILY_REPORT_{t_start.day}_{t_start.month}_{t_start.year}__{t_end.day}_{t_end.month}_{t_end.year}.pdf')
print(f'{analized_station} REPORT IS DONE')

###########################################################CALCULATING_HOURLY_SEISMOGRAMS###########################################################

print('------- DRAW HOURLY SEISMOGRAMS -------')

channels = ['z', 'n', 'e']

for t in time:

    #for data paths month below 10 will be: 01, 02, 03,...
    if t.month < 10:
        month = f'0{t.month}'
    else:
        month = t.month

    for sat in range (0,24):

        print(f'------- DRAW HOURLY SEISMOGRAMS FOR {t} {sat}h -------')

        #for plotting daily data
        fig, ax = plt.subplots(3,1,figsize=(30, 20))

        for i in channels: #loop through all channels

            #reading MSEED files
            if sat < 10:
                st = ob.read(out_SANDI_path + '/' + f'godina_{t.year}' + '/' + f'mjesec_{month}' + '/' + f'dan_{t.day}' + '/' + f'sat_0{sat}' +  '/' + f'{analized_station}_{i}_100_{t.year}{month}{t.day}_0{sat}00.mseed')
            else:
                st = ob.read(out_SANDI_path + '/' + f'godina_{t.year}' + '/' + f'mjesec_{month}' + '/' + f'dan_{t.day}' + '/' + f'sat_{sat}' +  '/' + f'{analized_station}_{i}_100_{t.year}{month}{t.day}_{sat}00.mseed')

            #get sample_rate and dataquality
            sample_rate = st[0].stats.sampling_rate #get sample rate in Hz

            #The actual data is stored as a ndarray in the data attribute of each trace.
            #print(st[0].data)
            y = st[0].data
            x = np.arange(0,len(y),1)

            #time_ticks=np.arange(0,len(x),sample_rate*60*60)
            #if len(time_ticks) != 25: #if data quantity is lower that it should be for 24 hours
            #    x,y,time_ticks = test_time_ticks(sample_rate,x,y) #set no data to np.nan

            #plot mseed seismic activity data on y-axis and time on x-axis
            plt.suptitle(f'{analized_station_net}_{analized_station}_{i}_{t}', fontsize=30)
            ax[channels.index(i)].set_xlabel ('Time (h)', fontsize=25)
            ax[channels.index(i)].set_ylabel (f'{i} (count)', fontsize=25)
            ax[channels.index(i)].plot(x,y)
            #ax[channels.index(i)].set_xticks(time_ticks) #x_axis in hours
            #ax[channels.index(i)].set_xticklabels(np.arange(0,25,1), fontsize=25)
            
            #ax[channels.index(i)].set_xlim(0,sample_rate*60*60*24) # sample_rate*minutessample_rate*60*60*24
            ax[channels.index(i)].tick_params(axis='y', labelsize=25)
            ax[channels.index(i)].grid()

            #garbage collection and deletition of obspy variable to save memory
            del st
            gc.collect()

        plt.savefig(f'{picture_path}/{analized_station_net}_{analized_station}_{t.day}_{t.month}_{t.year}_{sat}h_hourly_data.png')
        plt.close(fig) #close figure to save memory
        print(f'DONE - {analized_station_net}_{analized_station}_{t.day}_{t.month}_{t.year}_{sat}h_hourly_data')

        ###########################################################CALCULATING_HOURLY_PDF/PSD###########################################################

        print(f'------- DRAW HOURLY PDF/PSD - {t} {sat}h -------')

        for c in channels: #loop through all channels

            #reading MSEED data, selecting correct trace and metadata
            if sat < 10:
                st = ob.read(out_SANDI_path + '/' + f'godina_{t.year}' + '/' + f'mjesec_{month}' + '/' + f'dan_{t.day}' + '/' + f'sat_0{sat}' +  '/' + f'{analized_station}_{c}_100_{t.year}{month}{t.day}_0{sat}00.mseed')
            else:
                st = ob.read(out_SANDI_path + '/' + f'godina_{t.year}' + '/' + f'mjesec_{month}' + '/' + f'dan_{t.day}' + '/' + f'sat_{sat}' +  '/' + f'{analized_station}_{c}_100_{t.year}{month}{t.day}_{sat}00.mseed')
            
            #needed because of station network, name and chanel in trace
            if c == 'z':
                c = 'HHZ'
            elif c == 'n':
                c = 'HHN'
            elif c == 'e':
                c = 'HHE'

            tr = st.select(id=f"{analized_station_net}.{analized_station}..{c}")[0]
            inv = ob.read_inventory(f"/home/check_data/{analized_station}.xml")

            #initialize ppsd instance
            ppsd = PPSD(tr.stats, metadata=inv)
            ppsd.add(st) #add data

            ppsd.plot(f'{picture_path}/{analized_station_net}_{analized_station}_{c}_{t.day}_{t.month}_{t.year}_{sat}h_hourly_psd.png')
            print(f'DONE - {analized_station_net}_{analized_station}_{c}_{t.day}_{t.month}_{t.year}_{sat}h_hourly_psd')

###########################################################MAKE_PDF_HOURLY_REPORT###########################################################

print(f'------- MAKE HOURLY PDF REPORT -------')

#initializing pdf file
pdf = FPDF()

#channels list
channels = ['HHZ','HHN','HHE']

#set text font and size
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Times', 'B', size=20)

#first page of report is: weekly report and date: start - end
text_report = f"{analized_station} HOURLY REPORT"
text_date = f"DATE: {t_start.day}.{t_start.month}.{t_start.year} - {t_end.day}.{t_end.month}.{t_end.year}"

#centering and writing text_report and text_date
page_width = pdf.w
page_height = pdf.h
text_report_width = pdf.get_string_width(text_report)
text_date_width = pdf.get_string_width(text_date)

#write WEEKLY REPORT
x_position = (page_width - text_report_width) / 2
y_position = page_height / 2
pdf.text(x_position, y_position, text_report)

#write date span
x_position = (page_width - text_date_width) / 2
y_position += 10
pdf.text(x_position, y_position, text_date)


for t in time:
    for sat in range (0,24):
        pdf.add_page()
        pdf.image(f'{picture_path}/{analized_station_net}_{analized_station}_{t.day}_{t.month}_{t.year}_{sat}h_hourly_data.png', h=pdf.h/4.1, w=pdf.w - 20)
        pdf.ln(-6) #move image up (separate images on y axis)

        for c in channels: #STON has channels BHZ, BHN, BHE and rest of them have HHZ, HHN, HHE
            pdf.image(f'{picture_path}/{analized_station_net}_{analized_station}_{c}_{t.day}_{t.month}_{t.year}_{sat}h_hourly_psd.png', h=pdf.h/4.1, w=pdf.w - 20)
            pdf.ln(-6) #move image up (separate images on y axis)

pdf.output(f'/home/MSEED_files_analysis/reports/{analized_station}_HOURLY_REPORT_{t_start.day}_{t_start.month}_{t_start.year}__{t_end.day}_{t_end.month}_{t_end.year}.pdf')
print(f'{analized_station} REPORT IS DONE')
