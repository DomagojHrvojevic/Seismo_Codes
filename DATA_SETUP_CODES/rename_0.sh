#!/bin/bash

#Short bash script for making all names of files in folder ${directory}/${s}/HH0.D/ uppercase.

#Directory where the .msd files are located
directory="/mnt/storage/podaci/2024/DN"

#Loop through all stations
for s in UDBI PLIT; do

    #Loop through all channels
    for h in HH0.D; do

        #Loop through all .msd files in the specified directory
        for file in ${directory}/${s}/${h}/*.txt; do           

            #Check if the file exists (in case there are no .mse files)
            if [[ -f ${file} ]]; then                          

                #Name without .msd extension
                base_name=$(basename ${file} .txt)
                #Convert the filename to uppercase   #for making lower case file names: new_name=$(echo ${base_name} | tr '[:upper:]' '[:lower:]') 
                new_name=${base_name^^}
                #Rename the file
                mv ${file} ${directory}/${s}/${h}/${new_name}.txt
                
                #Echo the progress
                echo "Renamed: ${file} -> ${directory}/${s}/${h}/${new_name}"

            fi

        done

    done

done 
#DONE