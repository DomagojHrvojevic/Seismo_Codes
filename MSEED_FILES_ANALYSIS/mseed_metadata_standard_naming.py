import obspy as ob
import os
import pandas as pd 
import itertools

#channels
channels = ['HHZ','HHN','HHE']

#set year for analysis
year = '2025'

#all paths:
stations_infile_path = '/home/DuFAULT/STATIONS/Station_list.csv'
data_path = '/mnt/2025_local_data' #data_path = '/mnt/d/storage/podaci'

#all networks of stations that have backup data for qc
dir_net = os.listdir(f'{data_path}/{year}')

#empty list for stations
stations_dir = []

#get all available stations that have backup data
for i in dir_net:
    stations_dir.append(os.listdir(f'{data_path}/{year}/{i}'))

#list of all available stations backup data for setup year
stations_dir = list(itertools.chain.from_iterable(stations_dir)) 

#read stations_infile_path
stations = pd.read_csv(stations_infile_path)

for s in stations_dir:

    #get analized_station network
    analized_station_net = stations.loc[stations['Station'] == s.upper()].iloc[0]['Network']
    
    #sorting all data in list according to julian date just to get STARTTIME and ENDTIME

    if s == 'STON':
        channels = ['BHZ','BHN','BHE']
    else:
        channels = ['HHZ','HHN','HHE']
        
    for c in channels:

        print(f'station={s}, channel = {c}')
        
        lista = sorted(os.listdir(data_path + '/' + year + '/' + analized_station_net + '/' + s + '/' + f'{c}.D'))
        
        #eliminate all files that have 'mseed' in them
        lista = [ x for x in lista if "mseed" not in x ]

        for i in lista:

            st = ob.read(data_path + '/' + year + '/' + analized_station_net + '/' + s + '/' + f'{c}.D' + '/' + i)

            #print(st[0].stats)
            #print('--------------------')
            
            #there can be multiple traces in one mseed file
            for stat in st:

                #renaming stats parameters
                stat.stats['station'] = s
                stat.stats['network'] = analized_station_net
                stat.stats['location'] = ''

            st.write(data_path + '/' + year + '/' + analized_station_net + '/' + s + '/' + f'{c}.D' + '/' + i, format='MSEED')
            