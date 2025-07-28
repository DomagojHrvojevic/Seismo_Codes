###########################################################DESCRIPTION###########################################################
"""
    Description:    Reading SOH files. Just a practice and for testing purposes.

    Author:         Domagoj H.

    Remark:         Important to add 'del st' and 'gc.collect()'. Without these commands, 
                    the code may be terminated due to excessive memory usage.

    Date:           28.1.2025.

    Web page:       https://docs.obspy.org/packages/obspy.io.mseed.html
"""

###########################################################PYTHON_LIBRARY###########################################################
import obspy as ob
import glob
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import gc
import os

###########################################################PYTHON_CODE###########################################################
#!/usr/bin/python3

#Path to dataset
data_path = '/home/MSEED_files_analysis/SOH'
save_path = '/home/MSEED_files_analysis/pictures/SOH'
folders = os.listdir(data_path)

#empty lists for appending data 
x = []
y = []

#predefinied variables
sample_rate = 0 # in Hz
quality = ''

for i in folders: #loop through all available folders

    files = os.listdir(data_path + '/' + i) #all files in folder
    files.sort() #sorting of files according to their days numbering

    #for plotting daily data
    fig, ax = plt.subplots(len(files),1,figsize=(30, 20))
    fig.subplots_adjust(hspace=0.5) #vertcal spacing
    b = 0 #counter

    for j in files:

        #reading files
        st = ob.read(data_path + '/' + i + '/' + j)
        #print(st[0].stats) #printing stats of input file

        #The actual data is stored as a ndarray in the data attribute of each trace.
        y = st[0].data
        x = np.arange(0,len(y),1)

        #plot mseed seismic activity data on y-axis and time on x-axis
        ax[b].set_title(j, fontsize=20)
        ax[b].set_ylabel (f'{i}', fontsize=20)
        ax[b].plot(x,y)
        ax[b].tick_params(axis='y', labelsize=20)
        ax[b].tick_params(axis='x', labelsize=20)
        ax[b].grid()

        #add one to counter
        b += 1

        #garbage collection and deletition of obspy variable to save memory
        del st
        gc.collect()

    plt.savefig(f'{save_path}/{i}.png')
    print(f'DONE - {i}')

#initializing pdf file
pdf = FPDF()

files = os.listdir(save_path) #all files in folder save_path

for i in files:
    pdf.add_page()
    pdf.image(f'{save_path}/{i}',h=pdf.h/2, w=pdf.w - 20)

print('PDF DONE')
pdf.output(save_path + "/SOH.pdf")
