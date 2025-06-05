###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for creating plots of data availability by using informations collected by ISPAQ python library.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version: Ubuntu-22.04
                    Python version: 3.8.19
                    pandas version: 1.5.3
                    numpy version: 1.24.4
                    datetime version: 5.5

    Date:           11.2.2025. - 26.2.2025.

    Web page:       /
"""

###########################################################PYTHON_LIBRARY###########################################################

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

startdate = sys.argv[1]
enddate = sys.argv[2]
stations = sys.argv[3:]

t1 = datetime.strptime(startdate, "%Y-%m-%d")
t2 = datetime.strptime(enddate, "%Y-%m-%d")

channels = ['HE','HZ','HN'] #use only 2 letters because STON stations chanels are: 'BHE','BHZ','BHN'
time = []

#get time date values
while t1<=t2:
    time.append(t1)
    t1 += timedelta(days=1)

for cha in channels:
    percent_availability = [[] for i in range(0,len(time)) ]

    for t1 in time:

        for sta in stations:
            try:
                infile = '/home/domagoj/check_data/csv/'+sta+'/customStats_myStations_'+t1.strftime("%Y-%m-%d")+'_simpleMetrics.csv'
                stats = pd.read_csv(infile)
                stats_dict = stats.to_dict('index')
                pom = True

                for k, stinfo in stats_dict.items():
                    target = stinfo['target']
                    metricName = stinfo['metricName']
                    value = stinfo['value']
                    channel = target[10:12] #use only 2 letters because STON stations chanels are: 'BHE','BHZ','BHN'

                    if channel == cha:
                        pom = False
                        if metricName=='percent_availability':
                            percent_availability[time.index(t1)].append(value) #apending available data
                            percent_availability[time.index(t1)].append(100-value) #apending missing data

                if  pom:
                    percent_availability[stations.index(sta)].append(0); percent_availability[stations.index(sta)].append(100-0)
            
            except Exception as e:
                print(e)
                value = np.nan
                percent_availability[time.index(t1)].append(0); percent_availability[time.index(t1)].append(100-0)
                continue

    fig=plt.figure(figsize=(30, 15))
    plt.rcParams.update({'font.size': 40})
    plt.title(f'Percent availability for channel {cha}',fontsize=50)

    days = np.arange(0,len(time))

    for idx, station_data in enumerate(percent_availability):

        if idx == 0:
            plt.bar(stations,station_data[0::2],width=0.5,color= 'green')
            plt.bar(stations,station_data[1::2],bottom=station_data[0::2],width=0.5,color= 'red')
        else:
            station_data_bottom = [100*idx for i in stations] #all data below currently plotting data
            plt.bar(stations,station_data[0::2],bottom= station_data_bottom,width=0.5,color= 'green')
            plt.bar(stations,station_data[1::2],bottom= [a + b for a,b in zip(station_data_bottom,station_data[0::2])],width=0.5,color= 'red')

    plt.yticks(plt.yticks()[0][:len(time)], [f'{i.date().day}.{i.date().month}.{i.date().year}' for i in time])  #center X-ticks

    plt.grid()

    fig.savefig('./PICTURES/'+cha+'.png')
