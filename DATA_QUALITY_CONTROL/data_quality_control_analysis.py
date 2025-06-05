###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for creating .pdf file of quality control analysis of seismological data and stations.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda ispaq environment.
                    OS version: Ubuntu-22.04
                    Python version: 3.8.19
                    pandas version: 1.5.3
                    numpy version: 1.24.4
                    fpdf version: 1.7.2
                    obspy version: 1.4.0
                    datetime version: 5.5

                    PYCHERON -> PROBLEMI S GFORTRANOM (ZASTARJELA VERZIJA), STARA VERZIJA PYTHONA
                    PYCHERON -> DATA BASE KORUMPIRAN -> PROBLEM S UCITAVANJEM NA WEB VIEWER

                    For compression of pdf file ghostscript is used. Firstly it is installed with command: 
                    sudo apt install ghostscript,
                    and than it is used at the end of this python script.

    Date:           11.2.2025. - 26.2.2025.

    Web page:       /
"""

###########################################################PYTHON_LIBRARY###########################################################

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import obspy as ob
from fpdf import FPDF
import pandas as pd
import subprocess
import sys
import os

###########################################################PYTHON_FUNCTIONS###########################################################

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#start and end date
startdate = sys.argv[1]
enddate = sys.argv[2]
active_stations = sys.argv[3:]

#start and end date
t1 = datetime.strptime(startdate, "%Y-%m-%d").date()
t2 = datetime.strptime(enddate, "%Y-%m-%d").date()

#channels
channels = ['HZ','HN','HE']

#paths
station_list_path = "/home/domagoj/DuFAULT/STATIONS/Station_list.csv"
report_path = '/home/domagoj/DATA_QUALITY_CONTROL/REPORTS'
ispaq_plot_path = '/home/domagoj/DATA_QUALITY_CONTROL/PICTURES'
PDF_PSD_path = '/home/domagoj/check_data/PDFs'

#initializing pdf file
pdf = FPDF()

#set text font and size
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font('Times', 'B', size=20)

#first page of report is: weekly report and date: start - end
text_report = "WEEKLY REPORT"
text_date = f"DATE: {t1.day}.{t1.month}.{t1.year} - {t2.day}.{t2.month}.{t2.year}"

#centering and writing text_report and text_date
page_width = pdf.w
page_height = pdf.h
text_report_width = pdf.get_string_width(text_report)
text_date_width = pdf.get_string_width(text_date)

#write WEEKLY REPORT
x_position = (page_width - text_report_width) / 2
y_position = page_height / 2
pdf.text(x_position, y_position, text_report)

#write date span
x_position = (page_width - text_date_width) / 2
y_position += 10
pdf.text(x_position, y_position, text_date)

#read station list for more station metadata
df = pd.read_csv(station_list_path)

#adding first page with ispaq data availability
pdf.add_page()
pdf.set_font('Times', 'B', size=20)
text = 'Weekly stations data availability - ISPAQ'
x_position = (page_width -  pdf.get_string_width(text)) / 2
y_position = 8
pdf.text(x_position, y_position, text)
pdf.ln(4) #spacing between pictures
pdf.image(ispaq_plot_path + f'/HZ.png',h=pdf.h/3.5, w=pdf.w - 20)
pdf.ln(3) #spacing between pictures
pdf.image(ispaq_plot_path + f'/HN.png',h=pdf.h/3.5, w=pdf.w - 20)
pdf.ln(3) #spacing between pictures
pdf.image(ispaq_plot_path + f'/HE.png',h=pdf.h/3.5, w=pdf.w - 20)

#adding second page with obspy detailed data availability
pdf.add_page()
pdf.set_font('Times', 'B', size=20)
text = 'Weekly stations data availability - OBSPY'
x_position = (page_width -  pdf.get_string_width(text)) / 2
y_position = 8
pdf.text(x_position, y_position, text)
pdf.ln(3) #spacing between pictures
pdf.image('./PICTURES/obspy_image.png', h=pdf.h*0.9, w=pdf.w-10)

#insert pictures of data quality control in pdf file
for i in active_stations:

    #get location name and network
    location = df['Location'][df.index[df['Station'] == i]].iloc[0]
    network = df['Network'][df.index[df['Station'] == i]].iloc[0]

    #new page for SimpleMetrics.csv plots
    pdf.add_page()
    pdf.set_font('Times', 'B', size=20)

    #station name and info
    text = i + f' - {location}'
    x_position = (page_width -  pdf.get_string_width(text)) / 2
    y_position = 8
    pdf.text(x_position, y_position, text)
    pdf.ln(5)

    for c in channels:
        pdf.image(ispaq_plot_path + f'/{i}{c}.png', h=pdf.h/3.5, w=pdf.w - 20)
        pdf.ln(5) #move image down by y = 5 (separate images on y axis)

    #new page for PDFs
    pdf.add_page()
    pdf.ln(5)
    
    for c in channels: #STON has channels BHZ, BHN, BHE and rest of them have HHZ, HHN, HHE
        if i == 'STON':
            if not os.path.exists(PDF_PSD_path + f'/{network}' + f'/{i}/{network}.{i}..B{c}.D.{t1}_{t2}_PDF.png'):
                pdf.image(f'{PDF_PSD_path}/no_PDFs/{c}_none.png',h=pdf.h/3.5, w=pdf.w - 20)
                pdf.ln(5) #move image down by y = 5 (separate images on y axis)
            else:
                pdf.image(PDF_PSD_path + f'/{network}' + f'/{i}/{network}.{i}..B{c}.D.{t1}_{t2}_PDF.png', h=pdf.h/3.5, w=pdf.w - 20)
                pdf.ln(5) #move image down by y = 5 (separate images on y axis)
        else:
            if not os.path.exists(PDF_PSD_path + f'/{network}' + f'/{i}/{network}.{i}..H{c}.D.{t1}_{t2}_PDF.png'):
                pdf.image(f'{PDF_PSD_path}/no_PDFs/{c}_none.png',h=pdf.h/3.5, w=pdf.w - 20)
                pdf.ln(5) #move image down by y = 5 (separate images on y axis)
            else:
                pdf.image(PDF_PSD_path + f'/{network}' + f'/{i}/{network}.{i}..H{c}.D.{t1}_{t2}_PDF.png', h=pdf.h/3.5, w=pdf.w - 20)
                pdf.ln(5) #move image down by y = 5 (separate images on y axis)

#adding description of QC parameters drawn in report on last page
pdf.add_page()
pdf.set_font('Times', 'B', size=20)
text = 'Simple metrics and QC variables description'
x_position = (page_width -  pdf.get_string_width(text)) / 2
y_position = 10
pdf.text(x_position, y_position, text)

#percent_availability description
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 10, 'Visualize data availability with Ispaq/percent_availability:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 12) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5,'The portion of data available for each day is represented as a percentage. 100% data available means full coverage of data for the reported start and end time. Quality control validity limit is 99%.',align='J')
pdf.set_xy(10, pdf.y) #set x and y coordinates of multi_cell [value in mm]
pdf.set_text_color(128, 128, 128)  #gray color of text
pdf.multi_cell(0, 5, 'NOTE: percent_availability will only be calculated for target-days that have metadata. If metadata is available but no data can be retrieved, then it will be marked as percent_availability=0. In this case, the quality code associated with that target cannot be determined from the data itself and must be inferred. ISPAQ will currently mark data from EarthScope (fdsnws) as quality "M" and data from all other sources as "D". We are aware that this may not be able to capture the complexity of possible quality codes and will work on improving the logic in a future release.',align='J')

#num_spikes description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'num_spikes:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'This metric uses a rolling Hampel filter, a median absolute deviation (MAD) test, to find outliers in a timeseries. The number of discrete spikes is determined after adjacent outliers have been combined into individual spikes. NOTE: not to be confused with the spikes metric, which is an SOH flag only. Quality control validity limit is 1000.',align='J')

#num_glitches description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'num_glitches:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'The number of times that the \'Glitches detected\' bit in the \'dq_flags\' byte is set within a miniSEED file. This metric can be used to identify data with large filled values that data users may need to handle in a way that they don\'t affect their research outcomes. Quality control validity limit is 1000.', align='J')

#num_gaps description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'num_gaps:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'This metric reports the number of gaps encountered within a 24-hour window. Quality control validity limit is 500.', align='J')

#num_overlaps description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'num_overlaps:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'This metric reports the number of overlaps encountered in a 24-hour window. Quality control validity limit is 1000.', align='J')

#sample_unique description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'sample_unique:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'This metric reports the number (count) of unique values in data trace over a 24-hour window. Quality control validity limit is 150.', align='J')

#Visualize data availability with Obspy description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'Visualize data availability with Obspy:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'ObsPy ships the obspy-scan script (automatically available after installation), which detects the file format (MiniSEED, SAC, SACXY, GSE2, SH-ASC, SH-Q, SEISAN, etc.) from the header of the data files. Gaps are plotted as vertical red lines, start times of available data are plotted as crosses - the data itself are plotted as horizontal lines. The script can be used to scan through 1000s of files (already used with 30000 files, execution time ca. 45min), month/year ranges are plotted automatically. It opens an interactive plot in which you can zoom in.', align='J')

#PDF/PSD description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=15)
pdf.text(20, pdf.y + 7, 'PDF/PSD:')
pdf.set_font('Times', size=12)
pdf.set_xy(10, pdf.y + 9) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'Probability density function plots and/or text output (controlled by PDF_Preferences in the preference file; or by --pdf_type, --pdf_interval, --plot_include on the command line). You must have local PSD files written in the format produced by the \'psd_corrected\' metric (below) or run it concurrently with \'psd_corrected\'. These files should be in a directory specified by the psd_dir entry in the preference file or by --psd_dir on the command line, or in the database specified by db_name.', align='J')

#sources of all variables - description
pdf.set_text_color(0, 0, 0)  #black color of text
pdf.set_font('Times', 'B', size=12)
pdf.text(20, 260, 'Sources:')
pdf.set_font('Times', size=12)
pdf.set_xy(40, 256.3) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'EarthScope (2025). ISPAQ: ', align='J')
pdf.set_font('Times', 'I', size=12)
pdf.set_xy(88, 256.3) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'IRIS Seismographic Processing and Analysis Queue. ', align='J')
pdf.set_font('Times', size=12)
pdf.set_xy(40, 261.5) #set x and y coordinates of multi_cell [value in mm]
pdf.multi_cell(0, 5, 'Available at: https://github.com/EarthScope/ispaq (Accessed: 17 February 2025).', align='J')

pdf.set_xy(40, 272) #set x and y coordinates of multi_cell [value in mm]
pdf.set_font('Times', size=12)
pdf.multi_cell(0, 5, 'OBSPY: Available at: https://docs.obspy.org/ (Accessed: 25 February 2025).', align='J')

print('WEEKLY REPORT IS DONE')
pdf.output(report_path + f"/WEEKLY_REPORT_{t1.day}_{t1.month}_{t1.year}__{t2.day}_{t2.month}_{t2.year}.pdf")

#strongest comperssion available used on WEEKLY_REPORT.pdf file
subprocess.run(f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile={report_path}/WEEKLY_REPORT_compressed.pdf {report_path}/WEEKLY_REPORT_{t1.day}_{t1.month}_{t1.year}__{t2.day}_{t2.month}_{t2.year}.pdf', shell=True)
print('WEEKLY_REPORT_compressed IS DONE')
