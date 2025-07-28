#DESCRIPTION: bash script for sending a report of all station problems in the form of a .txt file via email.

#!/bin/bash

#STARTTIME=$(date -d '1 day ago' +'%Y-%m-%d')
STARTTIME="2024-11-06" #fixate on specific date

# set the path of the file to attach
file_path="/home/check_data/status/Error_status_"${STARTTIME}".txt"

# set the sender email address
#toE="user@mail.com"

# set the subject of the email
subject="DN error status file for "${STARTTIME}

# send the email with attachment
mailx  -s "${subject}" "${toE}" < ${file_path}
