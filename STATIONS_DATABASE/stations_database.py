###########################################################DESCRIPTION###########################################################

"""
    Description:    Python code for making database of seismological stations, data and metadata.

    Author:         Domagoj Hrvojevic

    Remark:         Working with miniconda base environment.
                    OS version: Ubuntu-22.04
                    Python version: 3.12.7
                    sqlalchemy version: 2.0.38
                    pandas version: 2.2.3
                    numpy version: 2.2.0

    Date:           31.1.2025. - ...

    Web page:       /
"""

###########################################################PYTHON_LIBRARY###########################################################

import sqlalchemy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
from PIL import Image
import os
import io

###########################################################PYTHON_FUNCTIONS###########################################################

def df_to_db(df,db_file_name):

    """ 
        Short python function for creating 
        database from pandas dataframe.
    """

    #sqlalchemy for interacting with the database
    engine = sqlalchemy.create_engine(f'sqlite:///{db_file_name}.db',connect_args={"timeout": 10},echo=False)

    #dataframe to database
    df.to_sql(name='Stations', con=engine, if_exists="append", index=False)

    return

def insert_image(database_path,stations_location_pictures_path,image_name):
    
    """
        Short python function for inserting 
        png picture in SQLite database.
    """

    with open(stations_location_pictures_path + image_name, "rb") as file:
        binary_data = file.read() #BLOB (binary data)

    #connecting to SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    #UPDATE updates existing record:
    sql = f"UPDATE Stations SET Position = ? WHERE Location = ?"
    cursor.execute(sql, (binary_data,image_name[:-4]))

    conn.commit()
    conn.close()
    print(f"{image_name} inserted successfully!")

    return

def store_image(database_path,stations_location_pictures_path,image_name):

    """ 
        Short python function for inserting 
        png picture in SQLite database.
    """

    image = Image.open(stations_location_pictures_path + image_name)
    if image.mode not in ["RGB", "L"]:
        image = image.convert("RGB")

    #convert image to binary
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG", quality=75)  #compress and store image
    binary_data = img_byte_arr.getvalue()

    #store in SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    sql = f"UPDATE Stations SET Position = ? WHERE Location = ?"
    cursor.execute(sql, (binary_data,image_name[:-4]))
    
    conn.commit()
    conn.close()
    print("Image stored successfully!")

###########################################################PYTHON_CODE###########################################################

#!/usr/bin/python3

#paths
stations_data_path = '/home/DuFAULT/STATIONS/Station_list.csv'
stations_location_pictures_path = '/home/DuFAULT/STATIONS/stations_locations_pictures/'
database_path ='/home/STATIONS_database/Seizmo_stations.db'

#"""
#data from csv file turn to pandas DataFrame and than to database (.db file)

#list of all png pictures of stations locations
sta_loc_pic = os.listdir(stations_location_pictures_path)

#read temporary text file into pandas DataFrame
df= pd.read_csv(stations_data_path)

#adding another collumn which will have picuters of locations
df['Position'] = np.nan

#turn to dataframe to database
df_to_db(df,'Seizmo_stations')

#inserting png images in existing database
insert_image(database_path,stations_location_pictures_path,sta_loc_pic[0])

#data from file is implemented to database
print(f'DONE -> {stations_data_path}')
#"""
