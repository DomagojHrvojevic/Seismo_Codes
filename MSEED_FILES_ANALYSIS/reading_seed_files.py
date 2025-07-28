###########################################################DESCRIPTION###########################################################
"""
    Description:    Reading .MSEED files. Just a practice and for testing purposes.

    Author:         Domagoj H.

    Remark:         Important to add 'del st' and 'gc.collect()'. Without these commands, 
                    the code may be terminated due to excessive memory usage.

    Date:           28.1.2025.

    Web page:       https://docs.obspy.org/packages/obspy.io.mseed.html
"""

###########################################################PYTHON_LIBRARY###########################################################
import obspy as ob
import matplotlib.pyplot as plt
import numpy as np
import gc

###########################################################PYTHON_CODE###########################################################
#!/usr/bin/python3

#function for testing length of time ticks (if len(time_ticks) != 25)
def test_time_ticks(sample_rate,x,y):
    difference = sample_rate*60*60*24 - len(x) #frequency * time - len(x) -> total time steps that have no data
    full_array = np.empty(int(len(x)+difference + 1)) * np.nan #full_array has correct dimensions for plotting ground motion activity (for time steps with no data -> none is added)
    full_array[:y.size] = y #full_array set first existing values of ground motion
    y = full_array #assign full_array to y
    x =  np.arange(0, len(full_array),1) #setting size valid total time steps (time (s) * frequency (Hz))
    time_ticks=np.arange(0,len(x),sample_rate*60*60) #setting correct time_ticks so it can be hourly displayed
    return x,y,time_ticks

#Path to dataset
data_path = '/mnt/d/storage/podaci/2024/HR/ZBLJ' #'/mnt/d/storage/podaci/2024/HR/VSVC'
data_path_list=data_path.split('/')

#empty lists for appending data 
x = []
y = []

#predefinied variables
sample_rate = 0 # in Hz
quality = ''
channels = ['HHZ.D','HHN.D','HHE.D']

for j in range (310, 317): #loop through all available days

    #for plotting daily data
    fig, ax = plt.subplots(3,1,figsize=(30, 20))

    for i in channels: #loop through all channels

        #reading MSEED files
        st = ob.read(data_path + '/' + i + '/' + f'{data_path_list[5]}.{data_path_list[6]}..{i}.{data_path_list[4]}.{j}')
        #print(st[0].stats) #printing stats of input file

        #get sample_rate and dataquality
        sample_rate = st[0].stats.sampling_rate #get sample rate in Hz
        quality = st[0].stats.mseed['dataquality'] #get dataquality

        #MiniSEED specific metadata is stored in stats.mseed
        #for k, v in sorted(st[0].stats.mseed.items()):
        #    print("'%s': %s" % (k, str(v))) 

        #The actual data is stored as a ndarray in the data attribute of each trace.
        #print(st[0].data)
        y = st[0].data
        x = np.arange(0,len(y),1)

        #Write data back to disc or a file like object
        #st.write('Mini-SEED-filename.mseed', format='MSEED') 

        time_ticks=np.arange(0,len(x),sample_rate*60*60)
        if len(time_ticks) != 25: #if data quantity is lower that it should be for 24 hours
            x,y,time_ticks = test_time_ticks(sample_rate,x,y) #set no data to np.nan

        #plot mseed seismic activity data on y-axis and time on x-axis
        plt.suptitle(f'{data_path_list[5]}_{data_path_list[6]}_{data_path_list[4]}_{j}', fontsize=30)
        ax[channels.index(i)].set_xlabel ('Time (h)', fontsize=25)
        ax[channels.index(i)].set_ylabel (f'{i} (count)', fontsize=25)
        ax[channels.index(i)].plot(x,y, label=f'quality: {quality}')
        ax[channels.index(i)].set_xticks(time_ticks) #x_axis in hours
        ax[channels.index(i)].set_xticklabels(np.arange(0,25,1), fontsize=25)
        ax[channels.index(i)].set_xlim(0,sample_rate*60*60*24) # sample_rate*minutessample_rate*60*60*24
        ax[channels.index(i)].tick_params(axis='y', labelsize=25)
        ax[channels.index(i)].legend(loc='upper right', fontsize=25)
        ax[channels.index(i)].grid()

        #garbage collection and deletition of obspy variable to save memory
        del st
        gc.collect()

    plt.savefig(f'{data_path_list[5]}_{data_path_list[6]}_{data_path_list[4]}_{j}.png')
    plt.close(fig) #close figure to save memory
    print(f'DONE - {data_path_list[5]}_{data_path_list[6]}_{data_path_list[4]}_{j}')
