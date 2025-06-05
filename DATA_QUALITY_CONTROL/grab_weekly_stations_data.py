###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for extracting weekly stations data and making them available locally.
                    Modeled after code used for copying data remotely for formatting data for SANDI usage.
                        -> copy_data.py
                        -> data_modules.py

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version: Ubuntu-22.04
                    Python version: 3.8.19
                    pandas version: 1.5.3

    Date:           14.2.2025. - 26.2.2025.
"""

###########################################################PYTHON_LIBRARY###########################################################

import sys
import os, os.path, glob, time
from datetime import datetime, timedelta
import pandas as pd
import subprocess

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

###########################################################PYTHON_CODE###########################################################

#start and end date
startdate = sys.argv[1]
YYYY = int(startdate[:4])
enddate = sys.argv[2]
t1 = datetime.strptime(startdate, "%Y-%m-%d").date()
t2 = datetime.strptime(enddate, "%Y-%m-%d").date()

#read stations .csv file
stations_infile_path = "Station_list.csv"
stations = pd.read_csv(stations_infile_path)
#transform pandas dataFrame to dictionary
sta_dict = stations.to_dict('index')

#channels
channels = ['HHE','HHZ','HHN']
#list of dates
time = []

#add all dates in list
while t1<=t2:
    time.append(t1)
    t1 += timedelta(days=1)

#remote SSH connection details
remote_host = "XXX.XX.XX.XX"
remote_user = "user"
remote_password = "user_pass"
remote_port = 1024
remote_data_folder = "/mnt/storage/podaci"

#output folders
out_folder = "/mnt/storage/podaci"

#copy data from SSH server locally
for station, stinfo in sta_dict.items():
    stnm = stinfo['Station']
    snet = stinfo['Network']

    #go through all dates 
    for t in time:
        #search for simpleMetrics.csv files -> transfer them locally
        try:
            infile = '/home/domagoj/check_data/csv/' + stnm + '/customStats_myStations_' + t.strftime("%Y-%m-%d") + '_simpleMetrics.csv'
            outfile = '/home/domagoj/check_data/csv/' + stnm + '/customStats_myStations_' + t.strftime("%Y-%m-%d") + '_simpleMetrics.csv'
            if not os.path.exists('/home/domagoj/check_data/csv/' + stnm):
                os.makedirs('/home/domagoj/check_data/csv/' + stnm) #create folder if it doesn't exist

            scp_command = f"sshpass -p '{remote_password}' scp -P {remote_port} {remote_domagoj}@{remote_host}:{infile} {outfile}"
            scp_result = subprocess.run(scp_command, shell=True)

            if scp_result.returncode == 0:
                print(f"Copied {infile}")
            else:
                print(f"Failed to copy {infile}: {scp_result.stderr}")

        except Exception as e:
            print(f"Error processing file {remote_file}: {e}")
            continue

        #search and find .mseed files that are needed -> transfer them locally
        try:
            for year in range(YYYY, datetime.now().year + 1):
                #input folder
                remote_in_folder = f"{remote_data_folder}/{year}/{snet}/{stnm}"

                #output folder
                local_out_folder1 = os.path.join(out_folder, str(year), snet, stnm)

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
                                        remote_file_path = os.path.join(remote_folder_comp, filename)
                                        local_file_path = os.path.join(local_out_folder2, filename)
                                        
                                        scp_command = f"sshpass -p '{remote_password}' scp -P {remote_port} {remote_user}@{remote_host}:{remote_file_path} {local_file_path}"
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
            print(f"Error processing station {station}: {e}")
            continue
