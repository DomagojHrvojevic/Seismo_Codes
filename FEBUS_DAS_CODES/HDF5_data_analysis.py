###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for analysis of HDF5 data files recorded by FEBUS DAS instrument.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda base environment.
                    OS version:         Ubuntu-22.04
                    Python version:     3.12.7
                    pandas version:     2.2.3
                    numpy version:      2.2.0
                    h5py version:       3.13.0
                    imageio version:    2.37.0

    Date:           13.3.2025. - ...

    Web page:       HDF5 Quick Start Guide:     https://docs.h5py.org/en/latest/quick.html
                    numpy.meshgrid:             https://numpy.org/devdocs/reference/generated/numpy.meshgrid.html

"""

###########################################################PYTHON_LIBRARY###########################################################

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import os
import h5py as h5
import imageio.v2 as imageio

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#hdf5 data path:
data_path = '/mnt/FEBUS_data/SR_DS_2025-03-17_12-46-18_UTC_GL20.h5' #data_path = '/mnt/d/FEBUS_data/WATERFALL_2025-03-13_07-12-09_UTC.h5'
#pictures path:
pictures_path = '/home/FEBUS_DAS/pictures_GL20'
#gif path:
gif_path = '/home/FEBUS_DAS/gif'

#read HDF5 file
with h5.File(data_path, "r") as f:

    #the first and only key of KeysViewHDF5
    KeysViewHDF5 = list(f.keys())[0]

    #the first and only key of class h5py._hl.group.Group
    hdf5_group_key = list(f[KeysViewHDF5].keys())[0]

    #two keys in HDF5 group: Zone1 and time
    Zone1 = list(f[KeysViewHDF5][hdf5_group_key].keys())[0]
    time = list(f[KeysViewHDF5][hdf5_group_key].keys())[1]
    
    #get StrainRate variable from Zone1 group
    StrainRate = list(f[KeysViewHDF5][hdf5_group_key][Zone1])[0]
    
    #HDF5 dataset "StrainRate" -> behaves like numpy.array
    StrainRate_data = f[KeysViewHDF5][hdf5_group_key][Zone1][StrainRate]

    #loop through all time steps:
    for i in range (200,300):#(0,len(StrainRate_data)-16845):

        #number of ticks on x and y axis
        x_length = len(StrainRate_data[i][0])
        y_length = len(StrainRate_data[i])

        #make contour plot of StrainRate_data
        fig, ax = plt.subplots(figsize=(30, 10))
        
        #numpy meshgrid
        X, Y = np.mgrid[0:x_length, 0:y_length]

        #set title
        ax.set_title(f'----- {i} -----')

        #make contour plot of StrainRate_data with colorbar; StrainRate_data can be transposed (flip shape)
        contour_ticks = np.linspace(-2000, 2000, 20) #ticks on colorbar
        level_ticks = np.arange(-2000, 2000, 100) #ticks on contour graph
        contour = plt.contourf(X, Y, StrainRate_data[i].T, level_ticks, cmap=plt.cm.seismic, vmin=-10000, vmax=10000, extend='both')
        plt.colorbar(contour, ticks=contour_ticks)

        #save figure
        plt.savefig(f'{pictures_path}/StrainRate_data_{i}.png')

        #close plots:
        plt.close()

        #inform that contour plot is done
        print(f'DONE TIMESTEP - {i}')

#genarate gif from all png files
#sort all file names according to timestep
images = sorted(os.listdir(pictures_path))
#read all images with imageio.imread function
images = [imageio.imread(f'{pictures_path}/{i}') for i in images]
#incorporate and save all png files to gif
imageio.mimsave(f'{gif_path}/StrainRate_data_GL20.gif',images)

