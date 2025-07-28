"""
DESCRIPTION: Short python code for transfering all needed hourly data files of all stations that are important for determining earthquakes on PLIT station.
"""

import shutil
import os
import subprocess

IN_folder='/mnt/Downloads'
OUT_folder='/mnt/SANDI_PODACI/godina_2024/mjesec_08'

#Stations that are of uttmost importance for locating earthquakes on PLIT station
stations = ["PLIT", "UDBI", "OTOC", "KSY", "SLNJ", "PETR", "CERK", "RUJC", "NVLJ", "OZLJ", "KIJV", "MORI", "DUGI", "RIY", "BRJN", "HR01A", "HR02A", "BH09A", "BH11A", "BH13A"]


brojac = ''
#ZA PUH PODATKE (.mseed)
with open("/mnt/SANDI_PODACI/godina_2024/SANDI_08_2024_FROM_PUH.txt", "w") as FILE_main:
    for i in range (16,32): #for loop, each day
        FILE_main.write(f'{i}.08.2024\n')
        os.makedirs(OUT_folder + f'/dan_{i}', exist_ok=True)  #avoids error if directory exists

        for j in range (0, 24):
            if j < 10:
                j = f'0{j}'
            else:
                j = j
            os.makedirs(OUT_folder + f'/dan_{i}/sat_{j}', exist_ok=True)  #avoids error if directory exists
            FILE_main.write(f'sat_{j}:  ')

            for file_name in list(os.listdir(IN_folder + f'/dan_{i}_PUH/sat_{j}')):

                for station in stations:
                    if station.lower() in file_name.lower():
                        shutil.move(IN_folder + f'/dan_{i}_PUH/sat_{j}/' + file_name , OUT_folder + f'/dan_{i}/sat_{j}/' + file_name )
                        if station not in brojac:
                            FILE_main.write(f'{station}  ')
                            brojac += station
            
            brojac = '' #reseting brojac for new hour
            print(f'DONE PUH HOUR {j}')
            FILE_main.write('\n')
            subprocess.run(f'rm -f /mnt/SANDI_PODACI/godina_2024/mjesec_08/dan_{i}/sat_{j}/*Zone.Identifier', shell=True, check=True) #brisanje svih Zone.Identifier file-a

        print(f'DONE PUH DAY {i}')


brojac = ''
#ZA DRIVE PODATKE (.gcf)
with open("/mnt/SANDI_PODACI/godina_2024/SANDI_08_2024_FROM_DRIVE.txt", "w") as FILE_main:
    for i in range (16,32): #for loop, each day
        FILE_main.write(f'{i}.08.2024\n')
        os.makedirs(OUT_folder + f'/dan_{i}', exist_ok=True)  #avoids error if directory exists

        for j in range (0, 24):
            if j < 10:
                j = f'0{j}'
            else:
                j = j
            os.makedirs(OUT_folder + f'/dan_{i}/sat_{j}', exist_ok=True)  #avoids error if directory exists
            FILE_main.write(f'sat_{j}:  ')

            for file_name in list(os.listdir(IN_folder + f'/dan_{i}_DRIVE/sat_{j}')):

                for station in stations:
                    if station.lower() in file_name.lower():
                        shutil.move(IN_folder + f'/dan_{i}_DRIVE/sat_{j}/' + file_name , OUT_folder + f'/dan_{i}/sat_{j}/' + file_name )
                        if station not in brojac:
                            FILE_main.write(f'{station}  ')
                            brojac += station
            
            brojac = '' #reseting brojac for new hour
            print(f'DONE DRIVE HOUR {j}')
            FILE_main.write('\n')
            subprocess.run(f'rm -f /mnt/SANDI_PODACI/godina_2024/mjesec_08/dan_{i}/sat_{j}/*Zone.Identifier', shell=True, check=True) #brisanje svih Zone.Identifier file-a

        print(f'DONE DRIVE DAY {i}')
