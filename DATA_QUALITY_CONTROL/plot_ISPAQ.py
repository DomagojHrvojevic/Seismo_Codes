###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for plotting all useful informations collected by ISPAQ python library.

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
import gc

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

startdate = sys.argv[1]
enddate = sys.argv[2]
stations = sys.argv[3:]

t1 = datetime.strptime(startdate, "%Y-%m-%d")
t2 = datetime.strptime(enddate, "%Y-%m-%d")

channels = ['HE','HZ','HN']
time = []

while t1<=t2:
    time.append(t1)
    t1 += timedelta(days=1)

for sta in stations:
    for cha in channels:
        percent_availability = []; num_spikes =[]; glitches = []; num_gaps = []; num_overlaps = []; sample_unique = []
        colors = [[] for br in range (0,6)] #colors for each variable (if vaues are satisfactorily - bar is green, if not - bar is red)

        for t1 in time:
            try:
                infile = '/home/domagoj/check_data/csv/'+sta+'/customStats_myStations_'+t1.strftime("%Y-%m-%d")+'_simpleMetrics.csv'
                stats = pd.read_csv(infile)
                stats_dict = stats.to_dict('index')
                pom = True

                for k, stinfo in stats_dict.items():
                    target = stinfo['target']
                    metricName = stinfo['metricName']
                    value = stinfo['value']
                    channel = target[10:12]

                    if channel == cha:
                        pom = False
                        if metricName=='percent_availability':
                            percent_availability.append(value)
                            if value < 99:
                                colors[0].append('red')
                            else:
                                colors[0].append('green')

                        elif metricName=='num_spikes':
                            num_spikes.append(value)
                            if value <= 1000:
                                colors[1].append('green')
                            else:
                                colors[1].append('red')
                                
                        elif metricName=='glitches':
                            glitches.append(value)
                            if value <= 1000:
                                colors[2].append('green')
                            else:
                                colors[2].append('red')
                                
                        elif metricName=='num_gaps':
                            num_gaps.append(value)
                            if value <= 500:
                                colors[3].append('green')
                            else:
                                colors[3].append('red')
                                
                        elif metricName=='num_overlaps':
                            num_overlaps.append(value)
                            if value <= 1000:
                                colors[4].append('green')
                            else:
                                colors[4].append('red')
                                
                        elif metricName=='sample_unique':
                            sample_unique.append(value)
                            if value >= 150:
                                colors[5].append('green')
                            else:
                                colors[5].append('red')
                if  pom:
                    percent_availability.append(0); num_spikes.append(value); glitches.append(value)
                    num_gaps.append(value); num_overlaps.append(value); sample_unique.append(value) 
                    colors[0].append('red');colors[1].append('red');colors[2].append('red')
                    colors[3].append('red');colors[4].append('red');colors[5].append('red') 
            
            except Exception as e:
                print(e)
                value = 0
                percent_availability.append(value); num_spikes.append(value); glitches.append(value)
                num_gaps.append(value); num_overlaps.append(value); sample_unique.append(value)
                colors[0].append('red');colors[1].append('red');colors[2].append('red')
                colors[3].append('red');colors[4].append('red');colors[5].append('red') 
                continue

        fig=plt.figure(figsize=(30, 15))
        plt.rcParams.update({'font.size': 17})
        fig.suptitle(f'ISPAQ QC for {cha}', fontsize=40)

        ax = plt.subplot(2,3,1)
        plt.title('Percent availability')
        plt.bar(time,percent_availability, width=0.5, color=colors[0],edgecolor='black')
        #if variable is at any day red (unvalid) -> background of plot will be red; else it will be green (valid)
        if 'red' in colors[0]:
            ax.set_facecolor('lightcoral')
        else:
            ax.set_facecolor('lightgreen')
        plt.axhline(y = 99, color = 'r', linestyle = '-')
        plt.ylim([0,100])
        plt.grid()
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m'))

        ax = plt.subplot(2,3,2)
        plt.title('Number of spikes')
        plt.bar(time,num_spikes, width=0.5, color=colors[1],edgecolor='black')
        #if variable is at any day red (unvalid) -> background of plot will be red; else it will be green (valid)
        if 'red' in colors[1]:
            ax.set_facecolor('lightcoral')
        else:
            ax.set_facecolor('lightgreen')
        #if max number of spikes is in intervals [0,100>, [100,500>, and  above 500 (draw limit line), set y-axis limit
        if max(num_spikes) < 100:
            plt.ylim([0,100])
        elif max(num_spikes) < 500:
            plt.ylim([100,500])
        else:
            plt.axhline(y = 1000, color = 'r', linestyle = '-')
        plt.grid()
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m'))

        ax = plt.subplot(2,3,3)
        plt.title('Number of glitches')
        plt.bar(time,glitches, width=0.5, color=colors[2],edgecolor='black')
        #if variable is at any day red (unvalid) -> background of plot will be red; else it will be green (valid)
        if 'red' in colors[2]:
            ax.set_facecolor('lightcoral')
        else:
            ax.set_facecolor('lightgreen')
        #if max number of glitches is in intervals [0,100>, [100,500>, and  above 500 (draw limit line), set y-axis limit
        if max(glitches) < 100:
            plt.ylim([0,100])
        elif max(glitches) < 500:
            plt.ylim([100,500])
        else:
            plt.axhline(y = 1000, color = 'r', linestyle = '-')
        plt.grid()
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m'))

        ax = plt.subplot(2,3,4)
        plt.title('Number of gaps')
        plt.bar(time,num_gaps, width=0.5, color=colors[3],edgecolor='black')
        #if variable is at any day red (unvalid) -> background of plot will be red; else it will be green (valid)
        if 'red' in colors[3]:
            ax.set_facecolor('lightcoral')
        else:
            ax.set_facecolor('lightgreen')
        #if max number of num_gaps is in intervals [0,100>, [100,520> (draw limit line), and  above 500 (draw limit line), set y-axis limit
        if max(num_gaps) < 100:
            plt.ylim([0,100])
        elif max(num_gaps) < 500:
            plt.ylim([100,520])
            plt.axhline(y = 500, color = 'r', linestyle = '-')
        else:
            plt.axhline(y = 500, color = 'r', linestyle = '-')
        plt.grid()
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m'))

        ax = plt.subplot(2,3,5)
        plt.title('Number of overlaps')
        plt.bar(time,num_overlaps, width=0.5, color=colors[4],edgecolor='black')
        #if variable is at any day red (unvalid) -> background of plot will be red; else it will be green (valid)
        if 'red' in colors[4]:
            ax.set_facecolor('lightcoral')
        else:
            ax.set_facecolor('lightgreen')
        #if max number of num_overlaps is in intervals [0,100>, [100,500>, and  above 500 (draw limit line), set y-axis limit
        if max(num_overlaps) < 100:
            plt.ylim([0,100])
        elif max(num_overlaps) < 500:
            plt.ylim([100,500])
        else:
            plt.axhline(y = 1000, color = 'r', linestyle = '-')
        plt.axhline(y = 1000, color = 'r', linestyle = '-')
        plt.grid()
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m'))

        ax = plt.subplot(2,3,6)
        plt.title('Number of unique samples')
        plt.bar(time,sample_unique, width=0.5, color=colors[5],edgecolor='black')
        #if variable is at any day red (unvalid) -> background of plot will be red; else it will be green (valid)
        if 'red' in colors[5]:
            ax.set_facecolor('lightcoral')
        else:
            ax.set_facecolor('lightgreen')
        plt.axhline(y = 150, color = 'r', linestyle = '-')
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%m'))
        plt.tight_layout()
        plt.grid()
        t1 = datetime.strptime(startdate, "%Y-%m-%d")

        #garbage collection and deletition of obspy variable to save memory
        plt.close()
        gc.collect()

        fig.savefig('./PICTURES/'+sta+cha+'.png')