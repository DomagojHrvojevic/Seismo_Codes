#!/usr/bin/env python

#module data_modules
#coding=utf-8

# Importing modules
from obspy import read
from obspy.core import UTCDateTime
from datetime import datetime, timedelta
import subprocess
import os, os.path, glob, time
import pandas as pd
import numpy as np

def read_network(infile):

	"""
    Read station elevation and location (lat-lon) from file named infile and
    save it to dictionary.

    :param infile: text file 6 columns in CSV format
                 1. station location
                 2. network code or name
                 3. station name 
                 4  station latitude
                 5. station longitude 
                 6. station elevation

    :return sta_dict: dictionary keyed by station names and values of stla, stlo and stel(in meters)
    """
    
    # Station file has to be comma delimeted
	stations = pd.read_csv(infile)
    # Convert the pandas dataFrame to dictionary
	sta_dict = stations.to_dict('index')
    
	return sta_dict
        
def get_files(data_folder, out_folder, stla, stlo, stel, stnm, snet, comp, conv_time):

	"""
    Convert recorded Scream data into hourly (suitable for SANDI) and daily mseed files.

    :param data_folder: folder with mseed files
    :param out_folder: main output folder for both hourly and daily files
    :param stla: station latitude
    :param stlo: station longitude
    :param stel: station elevation
    :param sntm: station name
    :param snet: network code or name
    :param comp: component of recorded data
    :param conv_time: date from when data is to be converted
    """

    # Get proper format of the station channel name
	if snet=='DN' or snet=='9H':
		cmpt = 'HH' + comp.upper()
	
	elif snet=='Y5':
		if comp == 'n':
			cmpt = 'HH1'
		elif comp == 'e':
			cmpt = 'HH2'
		else:
			cmpt = 'HHZ'

	elif snet=='CR':
		cmpt = 'BH' + comp.upper()

	# Path to recorded data
	in_folder = data_folder+"/"+snet+"/"+stnm+"/"+cmpt+".D"
	files = os.listdir(in_folder)
	conv_time = datetime.strptime(conv_time, "%d-%m-%Y")
	
	for file in files:
		# Check file date and run script for the newest files (from the date defined with conv_time)
		ft = file[-3:] + "-" + file[-8:-4]
		file_time = datetime.strptime(ft, "%j-%Y")  

		# Read recorded data
		if file_time == conv_time:
			st = read(os.path.join(in_folder,file), format='MSEED')

			# Merge traces and fill gaps with zeroes
			if len(st) > 1:
				st.merge(method=0, fill_value=None)
			if isinstance(st[0].data, np.ma.masked_array):
				st[0].data = st[0].data.filled()                    

			julday = st[0].stats.starttime.julday
			year = st[0].stats.starttime.year
			month = st[0].stats.starttime.month
			day = st[0].stats.starttime.day
			
			dt1 = UTCDateTime(str(year) + "-" + str(month) + "-" + str(day) + "T00:00:00.01")
			dt2 = UTCDateTime(str(year) + "-" + str(month) + "-" + str(day) + "T23:59:59.99")
			st = st.trim(dt1, dt2, pad=True, fill_value=None)
			if isinstance(st[0].data, np.ma.masked_array):
				st[0].data = st[0].data.filled()
				
			t_end = st[0].stats.endtime.hour
			hour = st[0].stats.starttime.hour
			
			# Write hourly files suitable for SANDI
			while hour < (t_end+1):
				dt = UTCDateTime(str(year) + "-" + str(month) + "-" + str(day) + "T" + str(hour) + ":00:00")
				st_cut = st.slice(dt, dt + 3600)

            	# Update headers in cut/hourly file
				st_cut[0].stats.stla = stla
				st_cut[0].stats.stlo = stlo
				st_cut[0].stats.stel = stel
				st_cut[0].stats.network = snet
				st_cut[0].stats.station = stnm
				if snet=='CR':
					st_cut[0].stats.channel = 'BH' + comp.upper()
				else:
					st_cut[0].stats.channel = 'HH' + comp.upper()

				# Output file name
				out_file = stnm.lower() + '_' + comp.lower() + '_' + str('%03i' % st_cut[0].stats.sampling_rate) + \
				"_" + str('%04i' % year) + str('%02i' % month) + str('%02i' % day) + "_" + str('%02i' % hour) + '00.mseed'

				# Output data folder
				out_folder1 = out_folder + '/godina_' + str(year) + '/mjesec_' + str('%02i' % month) + \
				'/dan_' + str('%02i' % day) + '/sat_' + str('%02i' % hour)

				if not os.path.exists(out_folder1):
					os.makedirs(out_folder1)
					print("Directory " , out_folder1,  " created.")

				# Write data
				st_cut.write(os.path.join(out_folder1, out_file), format='MSEED')
				print(out_file)
				hour += 1
				st_cut.clear()

			# Clear cache	
			st.clear()
