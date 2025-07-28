###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for assimilating two different data files: one from seiscomp and other from datalogger.
                    Seiscomp receives data via network connection from seismological station (seiscomp data).
                    Datalogger writes and stores values of seismological activity on itself (local data).
                    THIS IS THE SAME CODE AS: /home/MSEED_files_analysis/MSEED_files_assimilation.py, BUT FOR 
                    MERGING ANY FILES THAT ARE OBTAINED FROM SEISCOMP OR LOCALLY. JUST PUT PATHS WHERE DATA IN 
                    VARIABLES: seiscomp_data_path AND local_data_path. (origin of data not important)

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version:         Ubuntu-22.04
                    Python version:     3.8.19
                    obspy version:      1.4.0

                    Description of obspy function: Stream.merge(method=0, interpolation_samples=0):
                        ->  Discard data of the previous trace assuming the following trace contains data with a more correct time value. 
                            The parameter interpolation_samples specifies the number of samples used to linearly interpolate 
                            between the two traces in order to prevent steps. Note that if there are gaps inside, 
                            the returned array is still a masked array, only if fill_value is set, 
                            the returned array is a normal array and gaps are filled with fill value.
                            No interpolation (interpolation_samples=0):
                                                                        Trace 1: AAAAAAAA
                                                                        Trace 2:     FFFFFFFF
                                                                        1 + 2  : AAAAFFFFFFFF
                    
                    Parameter fill_value is set to 0, so data gaps will be filled with value 0.

    Date:           10.3.2025. - 25.3.2025.

    Web page:       For method in Stream.merge:     https://docs.obspy.org/packages/autogen/obspy.core.stream.Stream.merge.html#obspy.core.stream.Stream.merge
                                                    https://docs.obspy.org/packages/autogen/obspy.core.trace.Trace.html#obspy.core.trace.Trace.__add__
"""

###########################################################PYTHON_LIBRARY###########################################################

import subprocess
import os
import obspy as ob
import shutil

###########################################################PYTHON_FUNCTIONS###########################################################

def uppercase_file_name (file_extension,data_path):

    """
        Description:    Short python function that uses short bash script 
                        for renaming mseed files in correct manner.

        Input:          data_path = path of all files that have to be renamed correctly
                        file_extension = type of file or file extension (.msd,.mseed,...)

        Output:         correctly renaming of all files that are on data_path

        Remark:         All files on data_path have to be similarly named with same file extension.
    """

    #run bash command
    subprocess.run(f'/home/uppercase.sh {file_extension} {data_path}', shell=True)

    return

def mseed_status_update (station,network,data_path):

    """
        Description:    Short python function that corrects metadata of mseed files.
                        Standard naming for parameters: station, network and location.

        Input:          data_path = path of files that have datalogger default naming

        Output:         setting metadata of all files to standard nomenclature

        Remark:         Path data_path has to be standard path used on sysop-server.
                        example: /mnt/d/storage/podaci/2025/DN/DF04/HHE.D
    """

    #sorting all data in list according to julian date
    lista = sorted(os.listdir(data_path))

    #loop through all available files
    for l in lista:
        
        #obspy read mseed file
        st = ob.read(data_path + '/' + l)

        #if there are multiple traces in stream -> merge them in one trace
        if len(st) != 1:
            st.merge(method=1,fill_value=0,interpolation_samples=0)

        #checking mseed file stats
        #print(st[0].stats)

        #renaming stats parameters if network or station or location does not match standard nomenclature (through all traces!)
        if st[0].stats['network'] != network or st[0].stats['station'] != station or st[0].stats['location'] != '':
            st[0].stats['network'] = network
            st[0].stats['station'] = station
            st[0].stats['location'] = ''

            #save changed metadata (stats)
            st.write(data_path + '/' + l, format='MSEED')
        
        #if parameters match standard nomenclature
        else:
            st.clear()

        #just for tracking purposes
        print(f'STATS DONE FOR {l}')

    return

def data_availability (data_path):

    """
        Description:    Short python function that calculates data availability in percents.

        Input:          data_path = full path of mseed file

        Output:         data_availability_percent = daily data availability in percents

        Remark:         Path data_path has to be standard path used on sysop-server.
                        example: /mnt/d/storage/podaci/2025/DN/DF04/HHE.D
    """

    #read mseed file
    file = ob.read(data_path)

    #get sample rate in Hz (it should be the same for seiscomp and local data)
    sample_rate = file[0].stats.sampling_rate

    #total data timesteps in one day depending on sample_rate (number of values in daily seismogram)
    timesteps = sample_rate*60*60*24 

    #quantity of values in daily mseed file
    data_length = 0

    #get total quantity of daily local file values, time start and end of each segment
    for i in range (0,len(file)):
        data_length += len(file[i].data)

    #percent of daily data availability
    data_availability_percent = round(data_length/timesteps * 100,2) #in percents [%]

    return data_availability_percent

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#######################VARIABLES#######################

#seiscomp, local and assimilated data paths
seiscomp_data_path = '/mnt/d/testing_assimilation/seiscomp_data'
local_data_path = '/mnt/d/testing_assimilation/local_data'
assimilated_data_path = '/mnt/d/testing_assimilation/assimilated_data'

#variables:
channels = ['HHZ','HHN','HHE']

#locate local data and extract file extension
local_years = os.listdir(local_data_path)

#######################LOOP_THROUGH_FOLDERS#######################

#txt file for writing all print outputs; closed at the end of the block
with open(f"{assimilated_data_path}/mseed_files_assimilation.txt", "a") as txt_file:

    #loop through all available years that have local data
    for y in local_years:
        #all networks that have local files
        local_networks = os.listdir(f'{local_data_path}/{y}')

        #create folder in assimilated_data_path
        if not os.path.exists(f'{assimilated_data_path}/{y}'):
            os.mkdir(f'{assimilated_data_path}/{y}')

        #loop through all available networks
        for n in local_networks:
            #all stations that have local files
            local_stations = os.listdir(f'{local_data_path}/{y}/{n}')

            #create folder in assimilated_data_path
            if not os.path.exists(f'{assimilated_data_path}/{y}/{n}'):
                os.mkdir(f'{assimilated_data_path}/{y}/{n}')

            #loop through all available stations
            for s in local_stations:
                
                #create folder in assimilated_data_path
                if not os.path.exists(f'{assimilated_data_path}/{y}/{n}/{s}'):
                    os.mkdir(f'{assimilated_data_path}/{y}/{n}/{s}')

                #loop through all channels
                for c in channels:
                    print(f'--------------- {y}_{n}_{s}_{c} ---------------', file=txt_file)
                    #path of all local nad seiscomp files 
                    data_path_l = f'{local_data_path}/{y}/{n}/{s}/{c}.D'
                    data_path_s = f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D'

                    #create folder in assimilated_data_path
                    if not os.path.exists(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D'):
                        os.mkdir(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D')

                    #######################NOMENCLATURE_FUNCTIONS#######################

                    #all local files
                    local_files = os.listdir(data_path_l)
                    #all seiscomp files
                    seiscomp_files = os.listdir(data_path_s)
                    #defining file_extension variable for local and seiscomp data
                    file_extension_l = ''
                    file_extension_s = ''

                    #assuming that all files have same extensions (skipping if there is no files)
                    if local_files == [] and seiscomp_files == []:
                        print(f'NO LOCAL OR SEISCOMP AVAILABLE DATA', file=txt_file)
                        file_extension_l = ''
                        file_extension_s = ''
                        continue
                    elif local_files == []:
                        file_extension_s = seiscomp_files[0].split('.')[-1]
                        file_extension_l = ''
                    elif seiscomp_files == []:
                        file_extension_l = local_files[0].split('.')[-1]
                        file_extension_s = ''
                    else:
                        file_extension_l = local_files[0].split('.')[-1]
                        file_extension_s = seiscomp_files[0].split('.')[-1]

                    #msd or mseed or MSEED are valid file extensions -> files need to be processed
                    if 'msd' in file_extension_l or 'mseed' in file_extension_l or 'MSEED' in file_extension_l:
                        #firstly rename local mseed files and fix their stats
                        uppercase_file_name(file_extension_l,data_path_l)
                        mseed_status_update(s,n,data_path_l)
                    if 'msd' in file_extension_s or 'mseed' in file_extension_s or 'MSEED' in file_extension_s:                    
                        #seiscomp rename mseed files and fix their stats
                        uppercase_file_name(file_extension_s,data_path_s)
                        mseed_status_update(s,n,data_path_s)

                    #all local files naming has changed
                    local_files = os.listdir(data_path_l)
                    #seiscomp files naming has changed
                    seiscomp_files = os.listdir(data_path_s)

                    #######################UNIQUE_FILES#######################

                    #now compare two datasets and take all files that are unique to local or seiscomp files and copy them to final folder assimilated_data_path
                    #this is done so that assimilated data files will have data file for date at which seiscomp or local datasets does not have
                    unique_local_files = [f for f in local_files if f not in seiscomp_files]
                    unique_seiscomp_files = [f for f in seiscomp_files if f not in local_files]

                    #move all files that are unique to seiscomp or data logger with shutil.copyfile to corresponding assimilated_data_path
                    if len(unique_local_files) != 0:
                        for ulf in unique_local_files:
                            #local data availability 
                            local_data_availability = data_availability(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{ulf}')

                            shutil.copyfile(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{ulf}', f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{ulf}')
                            print(f'UNIQUE LOCAL FILE TAKEN: {ulf}; LOCAL AVAILABILITY: {local_data_availability}%, TOTAL AVAILABILITY: {local_data_availability}%', file=txt_file)
                            
                    if len(unique_seiscomp_files) != 0:
                        for usf in unique_seiscomp_files:
                            #seiscomp data availability 
                            seiscomp_data_availability = data_availability(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{usf}')

                            shutil.copyfile(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{usf}', f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{usf}')
                            print(f'UNIQUE SEISCOMP FILE TAKEN: {usf}; SEISCOMP AVAILABILITY: {seiscomp_data_availability}%, TOTAL AVAILABILITY: {seiscomp_data_availability}%', file=txt_file)

                    #######################DATA_AVAILABILITY#######################

                    #now files that are not unique needed to be compared; 
                    #missing data of file with greater data availability needs to be filled with data of file with lower data availability (if that file has that specific data)
                    data_files = [f for f in local_files if f not in unique_local_files] #all files that are present in local_files and seiscomp_files
                    for file in data_files:
                        #local and seiscomp mseed daily data availability in percents
                        local_data_availability = data_availability(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{file}')
                        seiscomp_data_availability = data_availability(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{file}')

                        #######################DATA_ASSIMILATION#######################

                        #data assimilation or data merge; data gaps will be filled with value 0
                        #check what file has greater data availability
                        if local_data_availability > seiscomp_data_availability: #local file has bigger percent of data availability
                            if local_data_availability == 100: #local file has no data gaps
                                shutil.copyfile(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{file}', f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}')
                                print(f'LOCAL FILE TAKEN: {file}; LOCAL AVAILABILITY: {local_data_availability}%, TOTAL AVAILABILITY: {local_data_availability}%', file=txt_file)
                            else: #local file has data gaps -> asimilate (merge) local and seiscomp files into one file
                                merged_file = ob.read(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{file}') #file containing less data availability
                                merged_file += ob.read(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{file}') #file containing more data availability
                                merged_file.sort(['starttime']) #sorting data traces
                                #merge mseed files (better described in DESCRIPTION part at begining) -> merging traces; gaps are filled with 0
                                merged_file.merge(method=1,fill_value=0,interpolation_samples=0)
                                merged_file.write(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}', format='MSEED') #write merged traces to one mseed file 
                                assimilated_data_availability = data_availability(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}') #new, assimilated data availability
                                print(f'FILES ARE ASSIMILATED: {file}; LOCAL AVAILABILITY: {local_data_availability}%, SEISCOMP AVAILABILITY: {seiscomp_data_availability}%, TOTAL AVAILABILITY: {assimilated_data_availability}%', file=txt_file)

                        elif local_data_availability < seiscomp_data_availability: #seiscomp file has bigger percent of data availability
                            if seiscomp_data_availability == 100: #seiscomp file has no data gaps
                                shutil.copyfile(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{file}', f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}')
                                print(f'SEISCOMP FILE TAKEN: {file}; SEISCOMP AVAILABILITY:{seiscomp_data_availability}%, TOTAL AVAILABILITY: {seiscomp_data_availability}%', file=txt_file)
                            else: #seiscomp file has data gaps -> asimilate (merge) local and seiscomp files into one file
                                merged_file = ob.read(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{file}') #file containing less data availability
                                merged_file += ob.read(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{file}') #file containing more data availability
                                merged_file.sort(['starttime']) #sorting data traces
                                #merge mseed files (better described in DESCRIPTION part at begining) -> merging traces; gaps are filled with 0
                                merged_file.merge(method=1,fill_value=0,interpolation_samples=0)
                                merged_file.write(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}', format='MSEED') #write merged traces to one mseed file 
                                assimilated_data_availability = data_availability(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}') #new, assimilated data availability
                                print(f'FILES ARE ASSIMILATED: {file}; LOCAL AVAILABILITY: {local_data_availability}%, SEISCOMP AVAILABILITY: {seiscomp_data_availability}%, TOTAL AVAILABILITY: {assimilated_data_availability}%', file=txt_file)
                        
                        else: #if both files have same data availability percents -> emphasis on local file 
                            if local_data_availability == 100: #local and seiscomp files have no data gaps (both have data availability = 100%)
                                shutil.copyfile(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{file}', f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}')
                                print(f'LOCAL FILE TAKEN: {file}; LOCAL AVAILABILITY: {local_data_availability}%, TOTAL AVAILABILITY: {local_data_availability}%', file=txt_file)
                            else: #there are some data gaps in both, local and seiscomp, data files
                                merged_file = ob.read(f'{seiscomp_data_path}/{y}/{n}/{s}/{c}.D/{file}') #file containing same data availability
                                merged_file += ob.read(f'{local_data_path}/{y}/{n}/{s}/{c}.D/{file}') #file containing same data availability, emphasis on local
                                merged_file.sort(['starttime']) #sorting data traces
                                #merge mseed files (better described in DESCRIPTION part at begining) -> merging traces; gaps are filled with 0
                                merged_file.merge(method=1,fill_value=0,interpolation_samples=0)
                                merged_file.write(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}', format='MSEED') #write merged traces to one mseed file 
                                assimilated_data_availability = data_availability(f'{assimilated_data_path}/{y}/{n}/{s}/{c}.D/{file}') #new, assimilated data availability
                                print(f'FILES ARE ASSIMILATED: {file}; LOCAL AVAILABILITY: {local_data_availability}%, SEISCOMP AVAILABILITY: {seiscomp_data_availability}%, TOTAL AVAILABILITY: {assimilated_data_availability}%', file=txt_file)


