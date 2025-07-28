#!/bin/bash

#Short bash script for making all names of .mseed files in ${directory}/${s}/${h}/ uppercase and removing .mseed extension.

#mseed type file, extension of file
mseed=$1

#Directory where the .msd files are located
directory=$2

#Loop through all .msd files in the specified directory
for file in ${directory}/*.${mseed}; do #Change file appendix accordingly

    #Check if the file exists (in case there are no .mse files)
    if [[ -f ${file} ]]; then                          

        #Name without .mseed extension
        base_name=$(basename ${file} .${mseed}) #Change file appendix accordingly             
        #Convert the filename to uppercase
        new_name=${base_name^^}                         
        #Rename the file
        mv ${file} ${directory}/${s}/${h}/${new_name}
        
        #Echo the progress
        echo "RENAMED: ${file} -> ${directory}/${s}/${h}/${new_name}"

    fi

done

#DONE