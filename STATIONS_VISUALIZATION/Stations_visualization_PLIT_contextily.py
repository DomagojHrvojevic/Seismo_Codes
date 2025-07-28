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
            /

    Koristene datoteke: 
            //wsl.localhost/Ubuntu-22.04/home/DuFAULT/STATIONS/stacoord.lst

    Pokretanje skripte: 
            python Stations_visualization_PLIT.py ili python3 Stations_visualization_PLIT.py
"""
#######################################PYTHON_LIBRARY#######################################
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiLineString
import contextily as ctx
import matplotlib.patheffects as pe
import matplotlib as mpl
from matplotlib.patches import Polygon as MplPolygon
import numpy as np 
import matplotlib.ticker as mticker
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

#postavljanje figure 
fig, ax = plt.subplots(figsize=(30, 30))

#GeoDataFrame
gdf = gpd.GeoDataFrame({"station": list(stations.keys()),"network":[value[0] for value in stations.values()]},geometry=[value[1] for value in stations.values()],crs="EPSG:4326")
#granicne lat,lon: (Min lon, Min lat, Max lon, Max lat)
#min_lon, min_lat, max_lon, max_lat = (gdf.geometry.x.min() - 0.2, gdf.geometry.y.min() - 0.1, gdf.geometry.x.max() + 0.2, gdf.geometry.y.max() + 0.1)
min_lon, min_lat, max_lon, max_lat = (14-0.0198, 43.75-0.015, 17+0.0198, 45.75+0.015) 

#crtanje tocaka na karti
#marker styles
marker_styles = {
    "Plit-net": {"marker": "^", "color": "red", "label": "Plit-net"}, 
    'Državna mreža': {"marker": "^", "color": "blue", "label": "Državna mreža"},
    "Privremene postaje": {"marker": "^", "color": "orange", "label": "Privremene postaje"}}

#plotanje pojedine lokacije postaje
for network, style in marker_styles.items():
    subset = gdf[gdf["network"] == network]  #filter network type
    subset.plot(ax=ax,markersize=1500,color=style["color"],marker=style["marker"],label=style["label"],path_effects=[pe.withStroke(linewidth=5, foreground="white")])

    #plotanje naziva postaja
    for _, row in subset.iterrows(): #iteracija po postajama u geodataframe-u
        ax.text(row.geometry.x,row.geometry.y-0.055,row["station"],color='black',fontsize=35,ha="center",path_effects=[pe.withStroke(linewidth=5, foreground="white")])

#legenda
ax.legend(fontsize=40,loc='lower left')

# Add your API key to the desired style from contextily providers
provider = ctx.providers.Stadia.StamenTerrainBackground(api_key="50f5dd92-87f7-40dc-96bf-f11736c3a215")

# Update the provider URL to include your API key
provider["url"] = provider["url"] + "?api_key={api_key}"

#postavljanje pozadinske karte
maps = ctx.add_basemap(ax, crs=gdf.crs, zoom=10, source=provider, attribution_size=15) #Some providers: Esri.WorldStreetMap, Esri.WorldImagery, NASAGIBS.BlueMarble, OpenStreetMap.Mapnik, OpenStreetMap.HOT, OpenTopoMap, CartoDB.Positron
#attribution positioning
txt = ax.texts[-1] #attribution text
txt.set_position([0.6,0.02]) #attribution text position (percents)

#granicne lat, lon
ax.set_xlim(min_lon, max_lon)
ax.set_ylim(min_lat, max_lat)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)

#formatiranje lat i lon tick-ova na x i y osi
def format_latitude(lat, pos):
    return f"{lat:.2f}°N"  #dodaje "°N" na lat tickove

def format_longitude(lon, pos):
    return f"{lon:.2f}°E"  #dodaje "°E" na lon tickove

#formatiranje tikova
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_latitude))  #lat -> y-os
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_longitude))  #lon -> x-os

#ucitavanje podataka
world = gpd.read_file('/home/DuFAULT/STATIONS/country_borders/PLIT_CRO_border.gpkg')
#podrucje interesa
countries_of_interest = world.cx[min_lon+0.0198:max_lon-0.0198, min_lat+0.015:max_lat-0.015]  # Longitude, Latitude
# crtanje hrvatske kopnene granice
countries_of_interest.plot(ax=ax, edgecolor='black', linewidth=4)

#granica NP Plitvice
NP_PLIT = gpd.read_file('/home/DuFAULT/STATIONS/country_borders/NP_PLIT.gpkg')
NP_PLIT.plot(ax=ax, edgecolor='black', linewidth=4, color='darkgreen')

#scale-bar
x, y, scale_len = max_lon-0.5, min_lat+0.07, 0.124524 #arrowstyle='-'
scale_rect = mpl.patches.Rectangle((x,y),scale_len,0.005,linewidth=1,edgecolor='k',facecolor='k',path_effects=[pe.withStroke(linewidth=5, foreground="white")])
ax.add_patch(scale_rect)
plt.text(x+scale_len/2, y+0.02, s='10 KM', fontsize=30, horizontalalignment='center',path_effects=[pe.withStroke(linewidth=5, foreground="white")])
#postavljanje strelice koja pokazuje prema sjeveru
ax.annotate("",xy=(x+scale_len*2, y+0.06),xytext=(x+scale_len*2, y+0.04),xycoords="data",arrowprops=dict(facecolor='black', arrowstyle="fancy,head_width=3,head_length=3,tail_width=1",path_effects=[pe.withStroke(linewidth=5, foreground="white")]))
plt.text(x+scale_len*2, y, s='N', fontsize=30, horizontalalignment='center',path_effects=[pe.withStroke(linewidth=5, foreground="white")])

####dodaj zebra frame####
xticks = ax.get_xticks() #x_ticks
yticks = ax.get_yticks() #y_ticks
#x-axis down - zebra border
for i in range(0,len(xticks)-1):
    if i == 0: #first line = black
        rect = mpl.patches.Rectangle((min_lon,min_lat),xticks[1]-min_lon,0.015,linewidth=1,edgecolor='black',facecolor='black') #(x,y),length, width
        ax.add_patch(rect)
    elif i == len(xticks)-1: #last line (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((xticks[i],min_lat),max_lon-xticks[i],0.015,linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
    else: #all lines in between (color depends on i)
        if i % 2 == 1:
            color = 'white'
        else:
            color = 'black'
        rect = mpl.patches.Rectangle((xticks[i],min_lat),xticks[i+1]-xticks[i],0.015,linewidth=1,edgecolor=color,facecolor=color) #(x,y),length, width
        ax.add_patch(rect)
#x-axis up - zebra border
for i in range(0,len(xticks)-1):
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
