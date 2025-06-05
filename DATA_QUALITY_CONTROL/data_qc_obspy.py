###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for creating plots of data availability by using informations collected by OBSPY python library.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version: Ubuntu-22.04
                    Python version: 3.8.19
                    obspy version: 1.4.0
                    datetime version: 5.5
                    pandas version: 1.5.3

    Date:           11.2.2025. - 26.2.2025.

    Web page:       /
"""

###########################################################PYTHON_LIBRARY###########################################################

from obspy.imaging.scripts.scan import Scanner
from datetime import datetime, timedelta
import pandas as pd
import obspy as ob
import subprocess
import sys
import os

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

#data path
data_path = '/mnt/storage/podaci'

#grab all inforamtion that is given at the start of program 
startdate = sys.argv[1]
enddate = sys.argv[2]
stations = sys.argv[3:]

#satrt and end date 
t1 = datetime.strptime(startdate, "%Y-%m-%d"); t_start = t1
t2 = datetime.strptime(enddate, "%Y-%m-%d"); t_end = t2
channels = ['HE','HZ','HN']
time = [];data = []
stnm = [];snet = []

#read stations .csv file
stations_infile_path = "/home/domagoj/DuFAULT/STATIONS/Station_list.csv"
stations_pd = pd.read_csv(stations_infile_path)
#transform pandas dataFrame to dictionary
sta_dict = stations_pd.to_dict('index')
for station, stinfo in sta_dict.items():
    stnm.append(stinfo['Station'])
    snet.append(stinfo['Network'])

#get time date values
while t1<=t2:
    time.append(t1)
    t1 += timedelta(days=1)

#get all mseed data files in one list
for year in range (t_start.year, t_end.year + 1):

    for station in stations:

        for channel in channels:
            
            if station == 'STON':
                path = data_path + f'/{year}/{snet[stnm.index(station)]}/{station}/B{channel}.D'
            else:
                path = data_path + f'/{year}/{snet[stnm.index(station)]}/{station}/H{channel}.D'

            #all mseed data files in folder path
            data_files = os.listdir(path)
            data_files = [ x for x in data_files if "Zone.Identifier" not in x ] #eliminate Zone.Identifier files

            for t in time:
                for file in data_files:
                    try:
                        #extract file name and convert to appropriate date for filtering
                        filename = os.path.basename(file)
                        file_time_str = filename[-3:] + "-" + filename[-8:-4]
                        file_time = datetime.strptime(file_time_str, "%j-%Y")

                        #add data file name to list
                        if file_time.strftime("%d-%m-%Y") == t.strftime("%d-%m-%Y"):
                            data.append(path + f'/{filename}')

                    except Exception as e:
                        #print(f"Error processing file {remote_file}: {e}")
                        continue

#make obspy data accessibility plot
data = ' '.join(data)
scp_result = subprocess.run(f"obspy-scan {data} -o /home/domagoj/DATA_QUALITY_CONTROL/PICTURES/obspy_image.png", shell=True)
