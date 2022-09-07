import folium
from folium.plugins import BeautifyIcon
import pandas as pd
import openrouteservice as ors


# First define the map centered around Beira
m = folium.Map(location=[-18.63680, 34.79430], tiles='cartodbpositron', zoom_start=8)

# Next load the delivery locations from CSV file at ../resources/data/idai_health_sites.csv
# ID, Lat, Lon, Open_From, Open_To, Needed_Amount
deliveries_data = pd.read_csv(
    'idai_health_sites.csv',
    index_col="ID",
    parse_dates=["Open_From", "Open_To"]
)

# Plot the locations on the map with more info in the ToolTip
for location in deliveries_data.itertuples():
    tooltip = folium.map.Tooltip("<h4><b>ID {}</b></p><p>Time spent: <b>{}</b></p>".format(
        location.Index, location.Needed_Amount
    ))

    folium.Marker(
        location=[location.Lat, location.Lon],
        tooltip=tooltip,
        icon=BeautifyIcon(
            icon_shape='marker',
            number=int(location.Index),
            spin=True,
            text_color='red',
            background_color="#FFF",
            inner_icon_style="font-size:12px;padding-top:-5px;"
        )
    ).add_to(m)

# The vehicles are all located at the port of Beira
depot = [-19.818474, 34.835447]

folium.Marker(
    location=depot,
    icon=folium.Icon(color="green", icon="bus", prefix='fa'),
    setZIndexOffset=1000
).add_to(m)
# Define the vehicles
# https://openrouteservice-py.readthedocs.io/en/latest/openrouteservice.html#openrouteservice.optimization.Vehicle
vehicles = list()
for idx in range(3):
    vehicles.append(
        ors.optimization.Vehicle(
            id=idx,
            start=list(reversed(depot)),
            # end=list(reversed(depot)),
            capacity=[300],
            time_window=[1553241600, 1553284800]  # Fri 8-20:00, expressed in POSIX timestamp
        )
    )

# Next define the delivery stations
# https://openrouteservice-py.readthedocs.io/en/latest/openrouteservice.html#openrouteservice.optimization.Job
deliveries = list()
for delivery in deliveries_data.itertuples():
    deliveries.append(
        ors.optimization.Job(
            id=delivery.Index,
            location=[delivery.Lon, delivery.Lat],
            service=1200,  # Assume 20 minutes at each site
            amount=[delivery.Needed_Amount],
            time_windows=[[
                int(delivery.Open_From.timestamp()),  # VROOM expects UNIX timestamp
                int(delivery.Open_To.timestamp())
            ]]
        )
    )
# Initialize a client and make the request
ors_client = ors.Client(key='5b3ce3597851110001cf6248464cb1ebbf014ddab25844b3211b925b')  # Get an API key from https://openrouteservice.org/dev/#/signup
result = ors_client.optimization(
    jobs=deliveries,
    vehicles=vehicles,
    geometry=True
)

# Add the output to the map
for color, route in zip(['green', 'red', 'blue'], result['routes']):
    decoded = ors.convert.decode_polyline(route['geometry'])  # Route geometry is encoded
    gj = folium.GeoJson(
        name='Vehicle {}'.format(route['vehicle']),
        data={"type": "FeatureCollection", "features": [{"type": "Feature",
                                                         "geometry": decoded,
                                                         "properties": {"color": color}
                                                         }]},
        style_function=lambda x: {"color": x['properties']['color']}
    )
    gj.add_child(folium.Tooltip(
        """<h4>Vehicle {vehicle}</h4>
        <b>Distance</b> {distance} m <br>
        <b>Duration</b> {duration} secs
        """.format(**route)
    ))
    gj.add_to(m)

folium.LayerControl().add_to(m)
m.save('map.html')