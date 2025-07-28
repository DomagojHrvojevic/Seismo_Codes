#!/bin/bash

#Short bash script for making all names of .msd files in ${directory}/${s}/${h}/ uppercase and removing .msd extension.

#Directory where the .msd files are located
directory="/mnt/storage/podaci/2024/DN"

#Loop through all stations
for s in UDBI PLIT; do

    #Loop through all channels
    for h in HHE.D HHN.D HHZ.D; do

        #Loop through all .msd files in the specified directory
        for file in ${directory}/${s}/${h}/*.msd; do           

            #Check if the file exists (in case there are no .mse files)
            if [[ -f ${file} ]]; then                          

                #Name without .msd extension
                base_name=$(basename ${file} .msd)              
                #Convert the filename to uppercase
                new_name=${base_name^^}                         
                #Rename the file
                mv ${file} ${directory}/${s}/${h}/${new_name}
                
                #Echo the progress
                echo "Renamed: ${file} -> ${directory}/${s}/${h}/${new_name}"

            fi

        done

    done

done 
#DONE
