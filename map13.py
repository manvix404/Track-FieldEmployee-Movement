import openrouteservice
from openrouteservice import convert
import folium
import json


client = openrouteservice.Client(key='5b3ce3597851110001cf6248464cb1ebbf014ddab25844b3211b925b')

coords = ((77.55911392868259,12.990561884233957),(77.58294798820391,12.959620977065718),(77.60589965753057,12.95679740202925),(77.64738241934802,12.986949642290451))
res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

m = folium.Map(location=[12.971893711921835, 77.59591523942986],zoom_start=10, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)

folium.Marker(
    location=list(coords[0][::-1]),
    popup="Galle fort time: 2hrs",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=list(coords[1][::-1]),
    popup="Jungle beach",
    icon=folium.Icon(color="red"),
).add_to(m)

folium.Marker(
    location=list(coords[2][::-1]),
    popup="Jungle beach",
    icon=folium.Icon(color="blue"),
).add_to(m)

folium.Marker(
    location=list(coords[3][::-1]),
    popup="Jungle beach",
    icon=folium.Icon(color="purple"),
).add_to(m)

print("jello")
m.save('map.html')