###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for testing DAS (distributed acoustic sensing) data files.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda das environment.
                    OS version:             Ubuntu-22.04
                    Python version:         3.12.9
                    DASPy-toolbox version:  1.1.2
                    h5py version:           3.13.0

                    DASDateTime is a subclass of the datetime.DateTime class and inherits all methods of datetime.DateTime

                    !!!WHEN TRANSFERRING DATA FROM FEBUS TO USB, AFTER TRANSFERRING PROCESS ENDED, LEAVE SOME TIME USB PLUGGED IN DAS!!!
                    !!!THAN SAFELY EJECT USB (IF EJECTION LASTS OVER FEW SECONDS, JUST KEEP WAITING UNTIL USB IS EJECTED)!!!
                                        !!!DATA WILL BE CORRUPTED IF USB IS NOT EJECTED SAFELY!!!
                                                !!!WAIT UNTIL USB IS EJECTED!!!

                    citate from web page: https://daspy-tutorial.readthedocs.io/en/latest/Denoising.html
                    Spikes are unusually large amplitudes and could be caused by laser frequency drift or laser noise. 
                    The spike removal function first applies the across-channel median filter and then the across-time 
                    median filter to generate a median map from the absolute amplitudes. Points with amplitudes exceeding 
                    a predefined threshold of the median map are identified as spikes. All spikes are subsequently 
                    substituted with interpolated values from adjacent channels.

    Date:           27.3.2025. - ...

    Web page:       https://daspy-tutorial.readthedocs.io/en/latest/index.html                                               
"""

###########################################################PYTHON_LIBRARY###########################################################

import matplotlib.pyplot as plt
import daspy as dp
import os

###########################################################PYTHON_FUNCTIONS###########################################################

def plot_hdf5_data(file_name, febus_data, part_of_title, saving_name, band_lower, band_higher):

    """
        Description:    Function for plotting febus hdf5 data in few ways:
                                - as waveform (strain-rate) [strain over distance (x-axis) through time (y-axis)]
                                - as spectrogram [amplitude of particular frequency over frequency (y-axis) per time (x-axis)]
                                - as waveform (strain-rate) but for bandpass(1,10)
                                - as spectrogram but for bandpass(1,10)

        Input parameters:
                                - file_name = name of hdf5 file
                                - febus_data = data of hdf5 file read with dp.read()
                                - part_of_title = name of method used for data analysis (spike_removal, downsampling or detrend)
                                - saving_name = string that goes at the end of png picture name indicating method used in data analysis
                                - band_lower = lower boundry for data bandpass (always at 1)
                                - band_higher = higher boundry for data bandpass (usually at 10, but for downsampling it is 2)
        
        Output parameters:
                                - one png containing 4 graphs: 2 waveforms and 2 spectrograms
    """

    #save figures (savefig path, dots-per-inch)
    fig, ax = plt.subplots(4, 1, figsize=(20,20))
    fig.subplots_adjust(wspace=1)
    print(f'------> plotting strain-rate for:{part_of_title}')
    ax[0].set_title(f'waveform{part_of_title}fs={febus_data.fs}Hz', fontsize = 10)
    febus_data.plot(ax=ax[0], obj='waveform', tmode='origin', dpi = 400) #tmode = determines how the time axis will be handled
    print(f'------> plotting spectrogram for:{part_of_title}')
    ax[1].set_title(f'spectrogram{part_of_title}fs={febus_data.fs}Hz', fontsize = 10)
    febus_data.plot(ax=ax[1], obj='spectrogram', dpi = 400)
    print(f'------> plotting waveform for bandpass for:{part_of_title}')
    febus_data_copy=febus_data.copy();febus_data_copy.bandpass(band_lower,band_higher)
    ax[2].set_title(f'waveform - bandpass {band_lower}-{band_higher} fs={febus_data.fs}Hz', fontsize = 10)
    febus_data_copy.plot(ax=ax[2], obj='waveform', dpi = 400)
    print(f'------> plotting spectrogram for bandpass for:{part_of_title}')
    ax[3].set_title(f'spectrogram - bandpass {band_lower}-{band_higher} fs={febus_data.fs}Hz', fontsize = 10)
    febus_data_copy.plot(ax=ax[3], obj='spectrogram', dpi = 400)
    print(f'------> save figure {file_name[:-3]}{saving_name}')
    plt.savefig(f'{save_data_path}/{file_name[:-3]}{saving_name}.png')
    plt.close()
    return

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#febus data path
febus_data_path = '/mnt/FEBUS_data/FEBUS_TWO_DAYS_WRITTING'
#save data path:
save_data_path = '/home/FEBUS_DAS/saved_figures'

#febus data files; sort them according to dates
febus_data_files = sorted(os.listdir(febus_data_path))

#loop through all file_names
for file_name in febus_data_files:

    #activate if condition for drawing specific new data from hdf5 files
    #if not os.path.exists(f'{save_data_path}/{file_name[:-3]}.png'):

    #read specific das file
    febus_data = dp.read(f'{febus_data_path}/{file_name}') # Read waveform example

    print('------------------')

    #plot original data
    plot_hdf5_data(file_name, febus_data, ' original_data ', '_original_data', 1, 10)

    print('------------------')

    #remove spikes in signal
    febus_data_spike_removal = febus_data.copy()
    febus_data_spike_removal.spike_removal()
    plot_hdf5_data(file_name, febus_data_spike_removal, ' spike_removal ', '_denoising', 1, 10)

    print('------------------')

    #data downsampling
    febus_data_downsampling = febus_data.copy()
    febus_data_downsampling.downsampling(tint=5)
    plot_hdf5_data(file_name, febus_data_downsampling, ' downsampling ', '_downsampling', 1, 2)

    print('------------------')

    #data detrend
    febus_data_spectrogram = febus_data.copy()
    febus_data_spectrogram.spectrogram(detrend=True, noverlap=156, nperseg=512) # overlap between two windows is 156 points
    plot_hdf5_data(file_name, febus_data_spectrogram, ' detrend ', '_detrend', 1, 10)

"""
#plotting data that is longer than one hour (2 hours) -> only for testing purposes
febus_data = dp.Collection(f'{febus_data_path}/WATERFALL_TEST_2025-03-25_*.h5') #all H5 files belonging to the same daily acquisition
febus_data=febus_data.select(stime=dp.DASDateTime(2025,3,25,16,0),etime=dp.DASDateTime(2025,3,25,18,0),meta_from_file='all',readsec=True)
plot_hdf5_data('WATERFALL_TEST_2025-03-25_2hours.h5', febus_data, ' ', '', 1, 10)
"""
"""
last part of code gives warnings, but the spectrogram and 
/home/miniconda3/envs/das/lib/python3.12/site-packages/daspy/core/section.py:124: UserWarning: The start time of the second Section (2025-03-25 16:20:52.348136+00:00) is inconsistent with the end time of the first Section (2025-03-25 16:56:49.471648+00:00).
  warnings.warn('The start time of the second Section '
/home/miniconda3/envs/das/lib/python3.12/site-packages/daspy/core/section.py:124: UserWarning: The start time of the second Section (2025-03-25 17:19:52.344498+00:00) is inconsistent with the end time of the first Section (2025-03-25 18:31:13.471648+00:00).
  warnings.warn('The start time of the second Section '
"""
