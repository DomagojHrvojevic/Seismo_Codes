"""
DESCRIPTION:    Short python code for removing all unnecessary hourly data files of all stations that are important for determining earthquakes on PLIT station.
                SANDI data for date: 26. - 30.9.2024.
"""

import shutil
import os
import subprocess

IN_folder='/mnt/SANDI_PODACI/godina_2024/mjesec_09'

#Stations that are of uttmost importance for locating earthquakes on PLIT station
stations = ["PLIT", "UDBI", "OTOC", "KSY", "SLNJ", "PETR", "CERK", "RUJC", "NVLJ", "OZLJ", "KIJV", "MORI", "DUGI", "RIY", "BRJN", "HR01A", "HR02A", "BH09A", "BH11A", "BH13A"]

for i in range (26,31): #for loop, each day
    for j in range (0, 24):
        if j < 10:
            j = f'0{j}'
        else:
            j = j

        for file_name in list(os.listdir(IN_folder + f'/dan_{i}/sat_{j}')):
            brojac = 0
            for station in stations:
                if station.lower() in file_name.lower():
                    brojac += 1 #station is in file name
            
            #check if data is from searched station, if not than delete that data
            if brojac == 0:
                print(f'delete {file_name}')
                subprocess.run(f'rm -f /mnt/SANDI_PODACI/godina_2024/mjesec_09/dan_{i}/sat_{j}/{file_name}', shell=True, check=True) #brisanje svih Zone.Identifier file-a
            else:
                brojac = 0

        print(f'DONE HOUR {j}')

    print(f'DONE DAY {i}')
