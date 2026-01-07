from pydoc import apropos

import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import functions


#read shapefile for ward boundaries
gdf = gpd.read_file("Wards/Wards.shp")

#read shapefile for air pollution risk 2023
apr2023_df = gpd.read_file("Web map data/Air pollution risk/2023/2023_air_pollution_risk.shp")

#Read shapefile for monitoring stations
ms_df = gpd.read_file("Web map data/Air pollution monitoring stations/CT_air_pollution_stations.shp")

#Read shapefile for SVI
svi_df = gpd.read_file("Web map data/SVI/SVI_export.shp")

#Create streamlit title
st.title("Cape Town Municipal Facilities")

option = st.selectbox(
    "Choose an option:",
    ["None","Air pollution risk", "Monitoring stations", "SVI"]
)

#Create folium map of cape town
m = folium.Map(location=[-33.9249, 18.4241], zoom_start=9, tiles="CartoDB positron")

# Inject CSS to hide the Ukrainian flag
m.get_root().html.add_child(folium.Element('<style> .leaflet-attribution-flag { display: none !important; } </style>'))

#Add ward boundaries to map
#functions.ward(dataframe=gdf, fields_name="WARD_NAME", aliases="Ward", map=m)

# Fit the map to the bounds of Cape Town
m.fit_bounds([[-34.35834, 18.30722], [-33.471276, 19.005338]])

match option:
    case "Air pollution risk":
        #add air pollution risk to map
        functions.areas(dataframe=apr2023_df, fields_name="Combined_2",
                        aliases="Air pollution risk:", map=m)
    case "Monitoring stations":
        #add monitoring stations to map
        functions.points(dataframe=ms_df, fields_name="Name",
                         aliases="Monitoring station:", map=m)
    case "SVI":
        # Add social vulnerability index to map
        functions.areas(dataframe=svi_df, fields_name="SVI", aliases="Social vulnerability index: ", map=m)

#display map
st_folium(m,width=700, height=500)