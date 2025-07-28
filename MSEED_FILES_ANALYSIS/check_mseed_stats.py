###########################################################DESCRIPTION###########################################################

"""
    Description:    Short python code for checking .MSEED files stats.
                    obspy version: 1.4.0

    Author:         Domagoj H.

    Date:           7.3.2025.

    Web page:       https://docs.obspy.org/packages/obspy.io.mseed.html
"""

###########################################################PYTHON_LIBRARY###########################################################

import obspy as ob
import os 

###########################################################PYTHON_CODE###########################################################
#!/usr/bin/python3

#Path to dataset that needs to be checked
data_path = '/mnt/d/storage/podaci/2024/DN' #INSERT PATH -> standard path used on server

#all available stations for testing
stations = os.listdir(data_path)

#predefinied variables
channels = ['HHZ.D','HHN.D','HHE.D']


for s in stations: #loop through all available stations

    for c in channels: #loop through all channels

        txt_file = open(f"{data_path}/{s}_{c}.txt", "w")

        #empty lists for appending data 
        files = os.listdir(data_path + '/' + s + '/' + c)
        
        for f in files:
                
            #reading MSEED files
            st = ob.read(data_path + '/' + s + '/' + c + '/' + f)

            #get mseed file stats #print(st[0].stats)
            stats = st[0].stats

            if stats.station != s:

                txt_file.write(f + '\n')
                txt_file.write(str(stats) + '\n')
                txt_file.write('\n')
        
        print(f'DONE {s}_{c}')
        txt_file.close()
