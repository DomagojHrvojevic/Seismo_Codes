###########################################################DESCRIPTION###########################################################

"""
    Description:    Short python code for checking .MSEED backup files stats.
                    This has been done only because files have different paths.
                    obspy version: 1.4.0
                    pandas version: 1.5.3
                    datetime version: 5.5

    Author:         Domagoj H.

    Date:           7.3.2025.

    Web page:       https://docs.obspy.org/packages/obspy.io.mseed.html
"""

###########################################################PYTHON_LIBRARY###########################################################

from datetime import datetime, timedelta
import pandas as pd
import obspy as ob
import os 

###########################################################PYTHON_CODE###########################################################
#!/usr/bin/python3

#Path to dataset that needs to be checked
data_path = '/mnt/stanice_backup' #INSERT PATH -> standard path used on server

#staions metadata path
stations_infile_path = '/home/DuFAULT/STATIONS/Station_list.csv'

#read stations_infile_path
stations_metadata = pd.read_csv(stations_infile_path)

#all available stations for testing
stations = os.listdir(data_path)

#eliminate stations_stats_txt (folder for savig txt files with info about stats) folder from stations folders
stations = [x for x in stations if 'stations_stats_txt' not in x]

#predefinied variables
channels = ['HHZ','HHN','HHE']


for s in stations: #loop through all available stations

    #station network
    analized_station_net = stations_metadata.loc[stations_metadata['Station'] == s.upper()].iloc[0]['Network']

    if s == 'mrcn' or s == 'strc' or s == 'trnv' or s == 'vtlj':

        #available years
        years = os.listdir(data_path + '/' + s + '/' + analized_station_net)

        for y in years:

            for c in channels: #loop through all channels

                print(f'DOING {s}_{y}_{c}', end = ' ')

                txt_file = open(f"{data_path}/stations_stats_txt/{s}_{y}_{c}.txt", "w")

                #empty lists for appending data 
                files = os.listdir(data_path + '/' + s + '/' + analized_station_net + '/' + y + '/' + analized_station_net + '/' + s + '/' + f'{c}.D')

                #eliminate files with wierd names
                files = [ x for x in files if "._" not in x ] #eliminate Zone.Identifier files
                
                for f in files:

                    #correct date of file
                    filename = os.path.basename(f)
                    file_time_str = filename[filename.index(y)+5 : filename.index(y)+8] + "-" + y
                    file_time = datetime.strptime(file_time_str, "%j-%Y")
                    DATE_TIME = file_time.strftime('%Y-%m-%d')
                        
                    #reading MSEED files
                    st = ob.read(data_path + '/' + s + '/' + analized_station_net + '/' + y + '/' + analized_station_net + '/' + s + '/' + f'{c}.D' + '/' + f)

                    #get mseed file stats #print(st[0].stats)
                    stats = st[0].stats

                    if stats.station.upper() != s.upper():

                        txt_file.write(f + '\t\tDATE: ' + DATE_TIME + '\n')
                        txt_file.write(str(stats) + '\n')
                        txt_file.write('\n')

                print(f'-> DONE {s}_{y}_{c}', end = '\n')
                txt_file.close()

    elif s == 'PLIT' or s == 'UDBI': #skip these stations because they have SANDI formated data, not station local data (backup data)
        continue

    else:

        #available years
        years = os.listdir(data_path + '/' + s)

        for y in years:

            for c in channels: #loop through all channels

                print(f'DOING {s}_{y}_{c}', end = ' ')

                txt_file = open(f"{data_path}/stations_stats_txt/{s}_{y}_{c}.txt", "w")

                #empty lists for appending data 
                files = os.listdir(data_path + '/' + s + '/' + y + '/' +  analized_station_net + '/' + s + '/' + c)

                #eliminate files with wierd names
                files = [ x for x in files if "._" not in x ] #eliminate Zone.Identifier files
                
                for f in files:
                    
                    #correct date of file
                    filename = os.path.basename(f)
                    file_time_str = filename[filename.index(y)+5 : filename.index(y)+8] + "-" + y
                    file_time = datetime.strptime(file_time_str, "%j-%Y")
                    DATE_TIME = file_time.strftime('%Y-%m-%d')
                        
                    #reading MSEED files
                    st = ob.read(data_path + '/' + s + '/' + y + '/' +  analized_station_net + '/' + s + '/' + c + '/' + f)

                    #get mseed file stats #print(st[0].stats)
                    stats = st[0].stats

                    if stats.station.upper() != s.upper():

                        txt_file.write(f + '\t\tDATE: ' + DATE_TIME + '\n')
                        txt_file.write(str(stats) + '\n')
                        txt_file.write('\n')

                print(f'-> DONE {s}_{y}_{c}', end = '\n')
                txt_file.close()

