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

    
### DATA_SETUP_CODES
  Codes used to organize data files (renaming, selecting, converting).


### FEBUS_DAS_CODES
  Programming Codes used to analyze data collected by DAS (Distributed Acoustic Sensing) instrument.


### ISPAQ_CODES
  Codes used to evaluate status of active seismological stations by using _ISPAQ_ python library.


### MSEED_FILES_ANALYSIS
  Codes for plotting, reading, naming, merging, formatting mseed data files.


### STATIONS_DATABASE
  Codes for creating database of seismological stations metadata.


### STATIONS_VISUALIZATION
  Codes for visualization of seismological stations on geospatial maps.




[^1]: [ISPAQ - Instrumental Seismic Performance Analysis using Quality metrics](https://github.com/insarag/ISPAQ)
[^2]: [ObsPy - A Python Toolbox for Seismology](https://github.com/obspy/obspy)
