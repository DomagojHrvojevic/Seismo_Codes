#######################################DESCRIPTION#######################################
"""
    Autor:  
            Domagoj Hrvojevic

    Datum:  
            18.12.2024. - 19.12.2024.

    Opis:   
            Python kod za kreaciju .GIF file-a koji prikazuje lokacije svih seizmoloskih postaja iz datoteke stations.gpkg.
            Svaka postaja ima svoj network, kod postaje i koordinate. Dodatne informacije se lako mogu dodati. Sve postavke 
            animacije koje se nalaze u kodu se mogu modificirati prema vlastitoj zelji i namjeri. 

    Napomena: 
            /

    Koristene biblioteke:
            GeoPandas: https://geopandas.org/ 
            Matplotlib: https://matplotlib.org/ 
            Contextily: https://contextily.readthedocs.io/en/latest/
            Pyproj: https://pyproj4.github.io/pyproj/stable/
            OpenStreetMap: https://www.openstreetmap.org/
            Numpy: https://numpy.org/

    Koristene datoteke: 
            //wsl.localhost/Ubuntu-22.04/home/DuFAULT/STATIONS/stations.gpkg

    Pokretanje skripte: 
            python Stations_visualization.py ili python3 Stations_visualization
"""
#######################################PYTHON_LIBRARY#######################################
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import patches
import contextily as ctx
from pyproj import CRS, Transformer
import numpy as np
from matplotlib.animation import PillowWriter
#######################################PYTHON_FUNCTIONS#######################################
#funkcija za update-anje frame-ova
def update(frame):
    #postavljanje info_box alpha = 0 (opacity = 0)
    global info_box, pulsation_count  #info_box = global variable

    print(frame)

    if frame < text_interval // frame_interval:
        #lokacija trenutne postaje 
        point = gdf.iloc[0]
        #x i y koordinate lokacije postaje
        x, y = point.geometry.x, point.geometry.y

    #pulsiranje -> velicina tocke
    if pulsation_count == 3:
        pulse_size = 100 
        pulsation_count -= 1 
    elif pulsation_count == 2:
        pulse_size = 200 
        pulsation_count -= 1 
    elif pulsation_count == 1:
        #reseriranje pulsation_count i pulse_size
        pulse_size = 100  
        pulsation_count = 3 

    #pulsirajuca tocka
    scatter.set_sizes([pulse_size])

    #info_box se update-a svakih 1000 ms
    if frame % (text_interval // frame_interval) == 0:
        #lokacija trenutne postaje 
        point = gdf.iloc[frame // (text_interval // frame_interval)]

        #x i y koordinate lokacije postaje
        x, y = point.geometry.x, point.geometry.y

        #update-anje plot-a
        scatter.set_offsets([(x, y)])

        #micanje zadnjeg info_box ako postoji
        if info_box:
            info_box.remove()

        #informacije koje se prikazuju u text-boxu
        info = f"Loc: {point['Location']}, Net: {point['Network']}, Sta: {point['Station']}, Lat: {point['Latitude']}, Lon: {point['Longitude']}, Ele: {point['Elevation']}"
        #update-anje plot-a
        scatter.set_offsets([(x, y)])
        #printanje info koji frame se radi
        print(point['Station'])
        #text-box za prikaz informacijavezano za svaku postaju 
        info_box = ax.text((x-x_min_limit)/(x_max_limit-x_min_limit), (y-y_min_limit)/(y_max_limit-y_min_limit)-0.02, '', ha='center', va='top', transform=ax.transAxes, fontsize=20, bbox=dict(facecolor='white', alpha=0.7))
        #update text-box info
        info_box.set_text(info)
    return scatter, info_box

#######################################PYTHON_CODE#######################################
#ucitavanje gpkg podataka putem geopandas
file_path = 'stations_active.gpkg'
gdf = gpd.read_file(file_path)
gdf = gdf.to_crs(epsg=3857)

#provjera da su ucitani podaci tocke
if gdf.geometry.iloc[0].geom_type != 'Point':
    raise ValueError("The GPKG file does not contain point data.")

#postavljanje subplota 
fig, ax = plt.subplots(figsize=(30, 20))
ax.set_xlim(gdf.total_bounds[0] - 10000, gdf.total_bounds[2] + 10000)  #X-granice
ax.set_ylim(gdf.total_bounds[1] - 10000, gdf.total_bounds[3] + 10000)  #Y-granice
ax.set_title('Seizmo-postaje', fontsize = 25, fontweight = 'bold')

#postavljanje min i max limita karte
x_min_limit = gdf.total_bounds[0] - 10000
x_max_limit = gdf.total_bounds[2] + 10000
y_min_limit = gdf.total_bounds[1] - 10000
y_max_limit = gdf.total_bounds[3] + 10000


#crtanje tocaka na karti
scatter = ax.scatter([], [], s=100, c='red', marker='o')

#postavljanje pozadinske karte
ctx.add_basemap(ax, zoom=10, source=ctx.providers.OpenStreetMap.Mapnik)

#text-box za prikaz informacijavezano za svaku postaju
info_box = None

#pulsacija tocke
pulsation_count = 3

#interval za tocku
frame_interval = 600 
#interval za info_box
text_interval = 1800 

#transformacija ax_ticks iz EPSG:3857 na EPSG:4326
transformer = Transformer.from_crs('EPSG:3857', 'EPSG:4326', always_xy=True)
#trenutni x i y tickovi
xticks = ax.get_xticks()
yticks = ax.get_yticks()

#transformiranje tickova u EPSG:4326 (longitude/latitude)
for i in range (0,len(xticks)-1):
    tick = transformer.transform(xticks[i], yticks[i])
    xticks[i]= tick[0]
    yticks[i]= tick[1]

#postavljanje tickova i labela
#ax.set_xticks(xticks)
#ax.set_yticks(yticks)
ax.set_xticklabels([f"{tick:.2f}°" for tick in xticks], fontsize = 20)
ax.set_yticklabels([f"{tick:.2f}°" for tick in yticks], fontsize = 20)


#izrada animacije
ani = FuncAnimation(fig, update, frames=len(gdf)*(text_interval//frame_interval), interval=frame_interval, repeat=True)

#spremajne animacije u gif podatak
ani.save('image.gif')
print('Animation = DONE')