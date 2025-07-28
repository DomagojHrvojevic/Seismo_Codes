#######################################PYTHON_LIBRARY#######################################
import folium
from shapely.geometry import Point
from branca.element import Template, MacroElement
#######################################PYTHON_CODE#######################################
#.lst data
file_path = '/home/DuFAULT/STATIONS/stacoord.lst'

#empty dictionary
stations={}

#station data: lat, lon
with open(file_path) as f:
    for line in f:
        item = list(line.split())
        key = item[0]
        lat = float(item[1])
        lon = float(item[2])
        geometry = Point(lon,lat)
        stations[key] = geometry #postaja = Point(lat,lon)

#create a base map centered around the stations
m = folium.Map(location=[stations['PLIT'].x, stations['PLIT'].y], zoom_start=8, tiles=None,control_scale = True)  # Base map without default tiles

#add Google Maps tiles # Replace `r` with: 'm' for standard map, 's' for satellite, 'h' for hybrid, 't' for terrain
folium.TileLayer(tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", attr="Google Maps",name="Google Maps",overlay=False,control=True).add_to(m)

#add markers for stations
#for station, point in stations.items():
folium.Marker(location=[stations['PLIT'].y, stations['PLIT'].x],icon=folium.Icon(color="red", icon="star"),).add_to(m)

#add layer control to switch basemaps
#folium.LayerControl().add_to(m)

#save map as HTML file or display
m.save("PICTURES/PLIT_folium.html")  # Save to file