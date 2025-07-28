# Seismo_Codes
Python and Bash codes used in seismological data quality control, DAS measured data, ispaq data metrics, mseed files analysis, stations database, formatting mseed files and seismological data processing.

## Description:

### DATA_QUALITY_CONTROL
  Set of codes used to develop quality control report of all active/chosen seismological stations.  
  
  <ins>**Scripts:**</ins>
  * `DATA_QC.sh:` Bash script that incorporates _grab_weekly_stations_data.py_, _run_ispaq.py_ from **ISPAQ** [^1] library, _plot_ISPAQ_availability.py_, _data_qc_obspy.py_, _plot_ISPAQ.py_ and _data_quality_control_analysis.py_ to create a quality control report for all ACTIVE seismological stations.
  * `data_qc_obspy.py:` Python code for creating plots of data availability by using information collected by **ObsPy** [^2] python library.
  * `data_quality_control_analysis.py:` Python code for creating a .pdf file of quality control analysis of active seismological stations based on collected data.
  * `grab_weekly_stations_data.py:` Python code for extracting weekly stations data and making them available locally.
  * `plot_ISPAQ.py:` Python code for plotting useful information collected by **ISPAQ** python library.
  * `plot_ISPAQ_availability.py:` Python code for creating plots of data availability by using information collected by **ISPAQ** python library.
  * `smartsolo_qc_obspy.py:` Python code that generate a pdf quality control analysis report of collected SmartSolo seismological stations data.
  * `stanice_backup_qc.py:` Python code for creating a pdf file of quality control analysis of seismological stations backup data.
  * `stanice_backup_qc_obspy.py:` Python code for generating PSD/PDF graphs with **ObsPy** for stations that haven't got one created from **ISPAQ**.
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
    <a href="WEEKLY_REPORT_17_3_2025__23_3_2025.pdf">Figure 1. An example of weekly quality control report</a>
  </p>

### DATA_SETUP_CODES
  Codes used to organize data files (renaming, selecting, converting).

<ins>**Scripts:**</ins>
  * `backup_DATA_check.py:` Short python code for comparing local files with existing files on server.
  * `rename_0.sh:` Short bash script for making all names of files in folder uppercase.
  * `rename_plit_udbi.sh:` Short bash script for making all names of .msd files in directory uppercase and removing .msd extension.
  * `SANDI_needed_data.py:` Short python code for removing all unnecessary hourly data files are not important for determining earthquakes on PLIT station.
  * `transfer_needed_sandi_station_data.py:` Similar code to _SANDI_needed_data.py_, including checks for missing data and logging the stations with absent data.
  * `uppercase.sh:` Similar code to _rename_0.sh_ with removing _.mseed_ extension.
  * `XML_to_RESP.py:` Python test code for converting station _.XML_ files into _.RESP_ files. Real _.RESP_ files are made from _.XML_ files, that are written in FDSN format, by using command **xml2resp** [^3] from evalresp toolbox.

## FEBUS_DAS_CODES
  Programming Codes used to analyze data collected by DAS (Distributed Acoustic Sensing) instrument.

<ins>**Scripts:**</ins>
  * `das_data_test.py:` Python code for testing DAS (distributed acoustic sensing) data files. Using **DASPy** [^4] for data plotting, spike removal, downsampling, and detrending, presented as both waveform and spectrogram, as shown in Figure 2.
  * `HDF5_data_analysis.py:` Python code for analysis of _HDF5_ data files recorded by FEBUS DAS instrument. Using **h5py** [^5] library for plotting StrainRate data and making them in gif with **imageio** [^6] library (figure 3).

<kbd>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/5e6ce2ce-0512-4c21-ba0b-2075f28037bc" width="20%">
    <img src="https://github.com/user-attachments/assets/a5f18c68-b938-4167-846f-51cf4b051fae" width="20%">
    <img src="https://github.com/user-attachments/assets/3df9871a-226d-41a8-b4c7-9722a6c27022" width="20%">
    <img src="https://github.com/user-attachments/assets/4b643d60-6304-43aa-9c05-86084f99c64d" width="20%">
  </p>
</kbd>
  <p align="center">
    Figure 2. An example showing the original DAS data, spike removal, downsampling, detrending, and bandpass filtering. The gauge length is set to 50 m.
  </p>

<kbd>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/9e30cb89-c9a9-411a-bca3-1a7ed2ce5a1d" width="100%">
  </p>
</kbd>
  <p align="center">
    Figure 3. Strain rate data recorded by the FEBUS DAS instrument, shown in GIF format. The gauge length is set to 20 m.
  </p>

## _CODES
  Codes used to evaluate status of active seismological stations by using **ISPAQ** python library.

<ins>**Scripts:**</ins>
  * `ISPAQ_Status.py:` Python code that reads the status .txt files simpleMetrics and PSDMetrics, and outputs errors for seismograph stations. A short error report is sent via email by running the Bash script _mail.sh_.
  * `ISPAQ_Status_test:` Simmilar to _ISPAQ_Status.py_ but for testing seismo-instruments.
  * `mail.sh:` Bash script to send a report of all station problems as a .txt file via email by using **mailx** [^7].
  * `PDF_run.sh:` Bash script for generating files and graphs of the power spectral density (PSD) and probability density function (PDF) for each seismic station using the **ISPAQ** library.
  * `PDF_run_test.sh:` Same as _PDF_run.sh_, but for testing seismo-instruments.
  * `run.sh:` Bash script for calculating customStats .csv files (data quality information). Then, the _ISPAQ_Status.py_ script condenses all SimpleMetrics information into a short error report, which is subsequently sent via email using the _mail.sh_ script.
  * `run_test.sh:` Simmilar to _run.sh_, but for testing seismo-instruments.
  * `run_v2.sh:` Similar to _run.sh_, but uses a different start-time variable.

## MSEED_FILES_ANALYSIS
  Codes for plotting, reading, naming, merging, formatting MiniSEED data files.

<ins>**Scripts:**</ins>
  * `backup_data_check_stats.py:` Python code for checking MiniSEED backup files stats.
  * `check_mseed_stats:` Python code for checking MiniSEED files stats.
  * `data_modules.py:` Python functions for converting recorded Scream data into hourly (suitable for SANDI) and daily mseed files.
  * `DF05_analysis.py:` Python code for the analysis of the DF05 station. Uses _data_modules.py_ The script performs the following tasks:
    * Transfers daily data from the server to the local machine
    * Converts daily data into hourly segments
    * Plots daily and hourly seismograms
    * Calculates daily and hourly Power Spectral Density (PSD) and Probability Density Function (PDF)
    * Generates daily and hourly summary reports
  * `format_smartsolo_to_sandi.py:` Formatting seismological data gathered by Smartsolo portable seismograph for SANDI software usage (hourly segments).
  * `MSEED_files_assimilation.py:` Python code for assimilating two different data files: one from seiscomp (network transfer) and other from datalogger (data recorder). Taking into account file naming, MiniSEED status, data availability.
  * `MSEED_files_assimilation_origin_not_important.py:` Similar to _MSEED_files_assimilation.py_, but this script is intended for merging two MiniSEED files of unknown origin.
  * `mseed_metadata_standard_naming.py:` Python code for correctly setting MiniSEED station metadata (network, station, location, channel).
  * `reading_seed_files.py:` Reading MiniSEED files with **ObsPy** library. Just a practice and for testing purposes.
  * `soh_plot_data.py:` Reading SOH files with **ObsPy** library. Just a practice and for testing purposes.

## STATIONS_DATABASE
  Codes for creating database of seismological stations metadata.
  
<ins>**Scripts:**</ins>
  * `stations_database.py:` Python code for making database of seismological stations, data and metadata. Using **sqlite3** [^8] python library. Contains functions for:
    * creating database from **pandas** [^9] dataframe
    * inserting/storing _.png_ picture in **SQLite** database (not practical)

## STATIONS_VISUALIZATION
  Codes for visualization of seismological stations on geospatial maps.

<ins>**Scripts:**</ins>
  * `PLIT_station_visualization_with_folium.py:` Plotting stations on base map with **Folium** [^10] python library.
  * `Stations_visualization.py:` Python code for creating a _.gif_ file that visualizes the locations of all seismic stations from the stations.gpkg file, with each station displaying its metadata. Python librarys **geopandas** [^11] and **contextily** [^12] are used.
  * `Stations_visualization_PLIT_basemap.py:` Python script for visualizing all seismo-stations locations for seismo-project. Using **geopandas** and **mpl_toolkits.basemap** libraries.
  * `Stations_visualization_PLIT_contextily.py:` Simmilar to _Stations_visualization_PLIT_basemap.py_, but this time using **geopandas** and **contextily**.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f4603cf5-5f38-4eb6-a29d-9ebc466452c5" height="220">
  <img src="https://github.com/user-attachments/assets/3ddd5e64-c0d7-458e-9998-3e7e7692f7e4" height="220">
  <img src="https://github.com/user-attachments/assets/783933b6-06a7-4524-9505-13150ea75bb6" height="220">
</p>
<p align="center">
  Figure 4. Stations plotted from left to right using **Basemap**, **Folium**, and **Contextily**.
</p>

### References
[^1]: [ISPAQ](https://github.com/EarthScope/ispaq) – Python command-line script that uses R packages to calculate seismology data quality metrics  
[^2]: [ObsPy](https://github.com/obspy/obspy) – Python toolbox for seismology and seismological observatories  
[^3]: [xml2resp](https://github.com/EarthScope/evalresp/blob/main/doc/xml2resp.1) – Converts StationXML input into RESP format  
[^4]: [DASPy](https://daspy-tutorial.readthedocs.io/en/latest/index.html) – Open-source package for Distributed Acoustic Sensing (DAS) data processing  
[^5]: [h5py](https://docs.h5py.org/en/latest/quick.html) – Container format for datasets and groups  
[^6]: [Imageio](https://pypi.org/project/imageio/) – Python library for reading and writing image data and scientific formats  
[^7]: [mailx](https://manpages.ubuntu.com/manpages/xenial/man1/bsd-mailx.1.html) – Intelligent mail processing system  
[^8]: [sqlite3](https://docs.python.org/3/library/sqlite3.html) – Lightweight disk-based SQL database  
[^9]: [pandas](https://pypi.org/project/pandas/) – Fast, flexible data structures for labeled/relational data  
[^10]: [Folium](https://python-visualization.github.io/folium/latest/) – Builds interactive maps using Leaflet.js  
[^11]: [GeoPandas](https://geopandas.org/en/stable/) – Easier handling of geospatial data in Python  
[^12]: [contextily](https://contextily.readthedocs.io/en/latest/) – Python package for adding basemaps to plots
