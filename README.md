# Seismo_Codes
Python and Bash codes used in seismological data quality control, DAS measured data, ispaq data metrics, mseed files analysis, stations database, formatting mseed files and seismological data processing.

## Descriptions:

### DATA_QUALITY_CONTROL
  Set of codes used to develop quality control report of all active/chosen seismological stations.  
  
  <ins>**Scripts:**</ins>
  * `DATA_QC.sh:` Bash script that incorporates _grab_weekly_stations_data.py_, _run_ispaq.py_ from **ISPAQ** [^1] library, _plot_ISPAQ_availability.py_, _data_qc_obspy.py_, _plot_ISPAQ.py_ and _data_quality_control_analysis.py_ to create a quality control report for all ACTIVE seismological stations.
  * `data_qc_obspy.py:` Python code for creating plots of data availability by using information collected by **OBSPY** [^2] python library.
  * `data_quality_control_analysis.py:` Python code for creating a .pdf file of quality control analysis of active seismological stations based on collected data.
  * `grab_weekly_stations_data.py:` Python code for extracting weekly stations data and making them available locally.
  * `plot_ISPAQ.py:` Python code for plotting useful information collected by **ISPAQ** python library.
  * `plot_ISPAQ_availability.py:` Python code for creating plots of data availability by using information collected by **ISPAQ** python library.
  * `smartsolo_qc_obspy.py:` Python code that generate a pdf quality control analysis report of collected SmartSolo seismological stations data.
  * `stanice_backup_qc.py:` Python code for creating a pdf file of quality control analysis of seismological stations backup data.
  * `stanice_backup_qc_obspy.py:` Python code for generating PSD/PDF graphs with **OBSPY** for stations that haven't got one created from **ISPAQ**.
<kbd>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/40bf37cb-4ceb-4056-acdd-afd699d5b4d6" width="20%">
    <img src="https://github.com/user-attachments/assets/fb54590e-7b1e-4966-8cd0-02e6796a1d50" width="20%">
    <img src="https://github.com/user-attachments/assets/a1681e60-9037-49a1-b38a-252d6f167197" width="20%">
    <img src="https://github.com/user-attachments/assets/34f8db1d-f26f-41ea-805f-da4a737485d4" width="20%">
    <img src="https://github.com/user-attachments/assets/a1f8350c-e5eb-4438-be28-bba07b01f0dd" width="20%">
    <img src="https://github.com/user-attachments/assets/c8e55808-a028-4dd0-8072-79cb99528326" width="20%">
    <img src="https://github.com/user-attachments/assets/62316ef2-1eda-4b2d-85fb-64c9adfc62a6" width="20%">
    <img src="https://github.com/user-attachments/assets/465c1858-9eea-42e0-aec0-23e0eea5677e" width="20%">
  </p>
</kbd>

  <p align="center">
    <a href="WEEKLY_REPORT_17_3_2025__23_3_2025.pdf"><strong>An example of weekly quality control report</strong></a>
  </p>





## DATA_SETUP_CODES
  Codes used to organize data files (renaming, selecting, converting).


## FEBUS_DAS_CODES
  Programming Codes used to analyze data collected by DAS (Distributed Acoustic Sensing) instrument.


## ISPAQ_CODES
  Codes used to evaluate status of active seismological stations by using _ISPAQ_ python library.


## MSEED_FILES_ANALYSIS
  Codes for plotting, reading, naming, merging, formatting mseed data files.


## STATIONS_DATABASE
  Codes for creating database of seismological stations metadata.


## STATIONS_VISUALIZATION
  Codes for visualization of seismological stations on geospatial maps.




[^1]: [ISPAQ - Python command line script that uses R packages to calculate seismology data quality metrics.](https://github.com/EarthScope/ispaq)
[^2]: [ObsPy - A Python Toolbox for seismology/seismological observatories](https://github.com/obspy/obspy)
