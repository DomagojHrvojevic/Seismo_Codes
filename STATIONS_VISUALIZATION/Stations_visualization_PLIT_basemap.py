#######################################DESCRIPTION#######################################
"""
    Autor:  
            Domagoj Hrvojevic

    Datum:  
            21. - 22.1.2024.

    Opis:   
            Python kod za kreaciju .png file-a koji prikazuje lokacije svih seizmoloskih postaja za PLIT projekt.
            Svaka postaja ima svoj network, kod postaje i koordinate. Dodatne informacije se lako mogu dodati.

    Napomena: 
            Engleski i hrvatski komentari unutar ovog python koda.

    Koristene datoteke: 
            //wsl.localhost/Ubuntu-22.04/home/DuFAULT/STATIONS/stacoord.lst

    Pokretanje skripte: 
            python Stations_visualization_PLIT.py ili python3 Stations_visualization_PLIT.py
"""
#######################################PYTHON_LIBRARY#######################################
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiLineString
import matplotlib.patheffects as pe
import matplotlib as mpl
from matplotlib.patches import Polygon as MplPolygon
import numpy as np 
import matplotlib.ticker as mticker
from mpl_toolkits.basemap import Basemap
import math as ma
#######################################PYTHON_CODE#######################################
#ucitavanje .lst podataka putem geopandas
file_path = '/home/DuFAULT/STATIONS/stacoord.lst'

#Postaje koje se trebaju nacrtati
stations_list = ["POBR","PLIT","UDBI", "OTOCA", "KSY", "SLNJ", "PETR", "CERK", "RUJC", "NVLJ", "OZLJ", "KIJV", "MORI", "DUGI", "RIY", "HR01A", "HR02A", "BH09A", "BH11A", "BH13A"]
stations_net = ['Privremene postaje','Plit-net','Plit-net','Plit-net','Privremene postaje','Privremene postaje','Privremene postaje','Privremene postaje','Privremene postaje','Privremene postaje','Državna mreža','Državna mreža','Državna mreža','Državna mreža','Državna mreža','Privremene postaje','Privremene postaje','Privremene postaje','Privremene postaje','Privremene postaje']

#prazan dictionary
stations={}

#citanje podataka: postaja, lat, lon
with open(file_path) as f:
    for line in f:
        item = list(line.split())
        key = item[0]
        if key in stations_list:
            stations[key] = [] #initialize empty list
            network = stations_net[stations_list.index(key)]
            lat = float(item[1])
            lon = float(item[2])
            geometry = Point(lon,lat)
            stations[key].append(network) #postaja = Point(lat,lon)
            stations[key].append(geometry) #postaja = Point(lat,lon)
#GeoDataFrame
gdf = gpd.GeoDataFrame({"station": list(stations.keys()),"network":[value[0] for value in stations.values()]},geometry=[value[1] for value in stations.values()],crs="EPSG:4326")

#postavljanje figure 
fig, ax = plt.subplots(figsize=(30, 30))
#granicne lat,lon: (Min lon, Min lat, Max lon, Max lat)
min_lon, min_lat, max_lon, max_lat = (14-0.0198, 43.75-0.015, 17+0.0198, 45.75+0.015) 
#projection, lat/lon extents and resolution of polygons to draw
#resolutions: c - crude, l - low, i - intermediate, h - high, f - full
map = Basemap(llcrnrlat=min_lat,llcrnrlon=min_lon,urcrnrlat=max_lat,urcrnrlon=max_lon,resolution='i',epsg='4326') #Basemap in epsg:3035 (https://epsg.io/3035)
#map World_Imagery
map.arcgisimage(service='World_Imagery', xpixels=10000) #backlayer map

#crtanje tocaka na karti
#marker styles
marker_styles = {
    "Plit-net": {"marker": "^", "color": "red", "label": "Plit-net"}, 
    'Državna mreža': {"marker": "^", "color": "blue", "label": "Državna mreža"},
    "Privremene postaje": {"marker": "^", "color": "orange", "label": "Privremene postaje"}}
#plotanje pojedine lokacije postaje
for network, style in marker_styles.items():
    subset = gdf[gdf["network"] == network]  #filter network type
    subset.plot(ax=ax,markersize=1300,color=style["color"],marker=style["marker"],label=style["label"])#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    #plotanje naziva postaja
    for _, row in subset.iterrows(): #iteracija po postajama u geodataframe-u
        ax.text(row.geometry.x,row.geometry.y-0.058,row["station"],color='white',weight='normal',fontsize=35,ha="center")#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
        if row["station"] == 'OTOCA':
            ax.text(row.geometry.x,row.geometry.y+0.028,'OTOC',weight='normal',color='white',fontsize=35,ha="center")#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
#attribution positioning
ax.text(max_lon-0.65, min_lat+0.04,"Esri, Maxar, Earthstar Geographics, and the GIS User Community",weight='normal',color='white',fontsize=20,ha="center")#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
#legenda
ax.legend(fontsize=40,loc='lower left')

#latitudes and longitudes drawn on map
ystep = 0.25 #lon-step
xstep = 0.5 #lat-step
parallels = np.arange(43.75,45.76,ystep) #make latitude lines od modela s pocetnim i konacnim (45.76 umjesto 45.75 zato da se napise posljednji tick na y-osi)
meridians = np.arange(14,17.1,xstep) #make longitude lines od modela s pocetnim i konacnim (17.1 umjseto 17 samo zato da napise posljednji tick na x-osi)
#setting x and y ticks
ax.set_xticks(meridians)
ax.set_yticks(parallels)
#font size for tick labels
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30) 
#formatiranje lat i lon tick-ova na x i y osi
def format_latitude(lat, pos):
    minutes = ma.floor((lat % 1)*60) #residual from degrees
    if minutes == 0: #if minutes are == 0 write it as 00
        minutes = '00'
    lat = ma.floor(lat)
    return f"{lat}°{minutes}\'N"  #dodaje "°N" na lat tickove
def format_longitude(lon, pos):
    minutes = ma.floor((lon % 1)*60) #residual from degrees
    if minutes == 0: #if minutes are == 0 write it as 00
        minutes = '00'
    lon = ma.floor(lon)
    return f"{lon}°{minutes}\'E"  #dodaje "°E" na lon tickove
#formatiranje tikova
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_latitude))  #lat -> y-os
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_longitude))  #lon -> x-os

#ucitavanje i crtanje podataka HRV granice
world = gpd.read_file('/home/DuFAULT/STATIONS/country_borders/clipped_CRO_PLIT_border.gpkg')
#podrucje interesa
countries_of_interest = world.cx[min_lon+0.0198:max_lon-0.0198, min_lat+0.015:max_lat-0.015]  # Longitude, Latitude
#crtanje hrvatske kopnene granice
countries_of_interest.plot(ax=ax, edgecolor='black', linewidth=5)
#ucitavanje i crtanje granica NP Plitvice
NP_PLIT = gpd.read_file('/home/DuFAULT/STATIONS/country_borders/NP_PLIT.gpkg')
NP_PLIT.plot(ax=ax, edgecolor='black', linewidth=5, color='darkgreen')

#crtanje kruga s radijusom od 50 Km oko postaje PLIT
PLIT_coord = gdf.loc[gdf["station"] == 'PLIT'] #kordinate Plitvica
PLIT_coord = PLIT_coord.to_crs(crs="EPSG:3035")  #Reproject to Web Mercator (in meters)
gdd = PLIT_coord.geometry.buffer(50000) #50000 m -> 50 Km
gdd = gpd.GeoSeries(gdd, crs="EPSG:3035").to_crs(crs="EPSG:4326")
gdd.plot(ax=ax, color='lightgray', alpha=0.25, edgecolor='white') #plot circle

#scale-bar notacija
x, y, scale_len = max_lon-0.4, max_lat-0.15, 0.124524 #arrowstyle='-'
scale_rect = mpl.patches.Rectangle((x,y),scale_len,0.007,linewidth=1,color='white')#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
ax.add_patch(scale_rect)
plt.text(x+scale_len/2, y+0.02, s='10 KM',weight='normal',fontsize=25, horizontalalignment='center',color='white')#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])
#postavljanje notacija strelice koja pokazuje prema sjeveru
ax.annotate("",xy=(x+scale_len*2, y+0.07),xytext=(x+scale_len*2, y+0.04),xycoords="data",arrowprops=dict(facecolor='white', arrowstyle="fancy,head_width=3,head_length=3,tail_width=1"))#,path_effects=[pe.withStroke(linewidth=3, foreground="white")]))
plt.text(x+scale_len*2, y, s='N',weight='normal', fontsize=30, horizontalalignment='center',color='white')#,path_effects=[pe.withStroke(linewidth=3, foreground="white")])

####dodaj zebra frame####
xticks = meridians #x_ticks
yticks = parallels #y_ticks
#x-axis down - zebra border
for i in range(0,len(xticks)):
    if i == 0: #first line = black
        rect = mpl.patches.Rectangle((min_lon,min_lat),xticks[1]-min_lon,0.015,linewidth=1,edgecolor='black',facecolor='black', alpha = 1) #(x,y),length, width
        ax.add_patch(rect)
    elif i == len(xticks)-1: #last line (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((xticks[i],min_lat),max_lon-xticks[i],0.015,linewidth=1,edgecolor=color,facecolor=color, alpha = 1) #(x,y),length, width
        ax.add_patch(rect)
    else: #all lines in between (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((xticks[i],min_lat),xticks[i+1]-xticks[i],0.015,linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
#x-axis up - zebra border
for i in range(0,len(xticks)):
    if i == 0: #first line = black
        rect = mpl.patches.Rectangle((min_lon,max_lat-0.015),xticks[1]-min_lon,0.015,linewidth=1,edgecolor='black',facecolor='black') #(x,y),length, width
        ax.add_patch(rect)
    elif i == len(xticks)-1: #last line (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((xticks[i],max_lat-0.015),max_lon-xticks[i],0.015,linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
    else: #all lines in between (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((xticks[i],max_lat-0.015),xticks[i+1]-xticks[i],0.015,linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
#y-axis left - zebra border
for i in range(0,len(yticks)-1):
    if i == 0: #first line = black
        rect = mpl.patches.Rectangle((min_lon,min_lat),0.0198,yticks[1]-min_lat,linewidth=1,edgecolor='black',facecolor='black') #(x,y),length, width
        ax.add_patch(rect)
    elif i == len(xticks)-1: #last line (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((min_lon,yticks[i]),0.0198,max_lat-yticks[i],linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
    else: #all lines in between (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((min_lon,yticks[i]),0.0198,yticks[i+1]-yticks[i],linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
#y-axis right - zebra border
for i in range(0,len(yticks)-1):
    if i == 0: #first line = black
        rect = mpl.patches.Rectangle((max_lon-0.0198,min_lat),0.0198,yticks[1]-min_lat,linewidth=1,edgecolor='black',facecolor='black') #(x,y),length, width
        ax.add_patch(rect)
    elif i == len(xticks)-1: #last line (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((max_lon-0.0198,yticks[i]),0.0198,max_lat-yticks[i],linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
    else: #all lines in between (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((max_lon-0.0198,yticks[i]),0.0198,yticks[i+1]-yticks[i],linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
####dodaj kvadratice na rubove - estetski####
rect = mpl.patches.Rectangle((min_lon,min_lat),0.0198,0.015,linewidth=1,edgecolor='grey',facecolor='grey') #(x,y),length, width
ax.add_patch(rect)
rect = mpl.patches.Rectangle((min_lon,max_lat-0.015),0.0198,0.015,linewidth=1,edgecolor='grey',facecolor='grey') #(x,y),length, width
ax.add_patch(rect)
rect = mpl.patches.Rectangle((max_lon-0.0198,min_lat),0.0198,0.015,linewidth=1,edgecolor='grey',facecolor='grey') #(x,y),length, width
ax.add_patch(rect)
rect = mpl.patches.Rectangle((max_lon-0.0198,max_lat-0.015),0.0198,0.015,linewidth=1,edgecolor='grey',facecolor='grey') #(x,y),length, width
ax.add_patch(rect)

#spremanje png / bbox_inches, pad_inches (no extra whitespace), dpi (png high resolution), transparent (prozirno)
fig.tight_layout()
plt.savefig('PICTURES/PLIT_station.png', transparent=True)#bbox_inches='tight',pad_inches=0)#, dpi=300)
