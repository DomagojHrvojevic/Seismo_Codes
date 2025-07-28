######################################################################################DESCRIPTION######################################################################################
"""
DATE: 6.12.2024

AUTHOR: Domagoj Hrvojević

DESCRIPTION:    This Python script converts station .XML files into .RESP files. These .RESP files are crucial for the bash script located
                at /home/run.sh, which utilizes the ISPAQ Python library to export _simpleMetrics.csv and _PSDMetrics.csv files.
                Both of these CSV files are subsequently processed by the Python program /home/ispaq/ISPAQ_Status.py to generate 
                a .txt report detailing the status and errors of seismograph stations. 
                
                User only needs to type ./run.sh in terminal and everything is automatically calculated and executed.

REMARK:     This is only for testing purposes. Real .resp files are made from .xml files, that are written in FDSN format, by using command 
            xml2resp from evalresp toolbox: 
                -> evalresp: https://github.com/EarthScope/evalresp
                -> xml2resp: https://github.com/EarthScope/evalresp/blob/main/doc/xml2resp.1

            If .xml files are in SCML (seiscomp) format, than it is necessary to use command fdsnxml2inv (from seiscomp software package) 
            which converts .xml file to FDSN format:
                -> fdsnxml2inv: https://www.seiscomp.de/doc/apps/fdsnxml2inv.html#fdsnxml2inv

            Take care in naming .resp files and separating each channel component in separate .resp files 
            (for example: RESP.DN.DF01..HHE -> RESP.{network.code}.{station.code}.{location}.{channel.code}).
"""
######################################################################################LIBRARY######################################################################################
from obspy.core.inventory import read_inventory
import os


######################################################################################MAIN_CODE######################################################################################
#load station XML file
inventory = read_inventory("/home/check_data/DF01.xml")

#output for RESP files for each channel
OUTPUT = 'TEST_RESP_FILES'

for network in inventory:
    for station in network:
        for channel in station:
            #generate RESP file name
            resp_file = os.path.join(OUTPUT,f"RESP.{network.code}.{station.code}..{channel.code}")
            resp_content = f"network={network.code}, station={station.code}, location=, channel={channel.code}, date={channel.start_date}"

            # Write to RESP file
            with open(resp_file, "w") as f:
                f.write(resp_content)

            print(f"Generated {resp_file}")
