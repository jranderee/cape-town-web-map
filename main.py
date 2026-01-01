import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import functions


#read shapefile for ward boundaries
gdf = gpd.read_file("Wards/Wards.shp")

#read shapefile for fire stations
fire_stations_df = gpd.read_file("Fire_Stations/Fire_Stations.shp")

#Read shapefile for healthcare facilities
health_df = gpd.read_file("Health_Care_Facilities/Health_Care_Facilities_(Clinics%2C_Hospitals).shp")

#Create streamlit title
st.title("Cape Town Municipal Facilities")

option = st.selectbox(
    "Choose an option:",
    ["None","Fire Stations", "Healthcare Facilities"]
)

#Create folium map of cape town
m = folium.Map(location=[-33.9249, 18.4241], zoom_start=9, tiles="CartoDB positron")

# Inject CSS to hide the Ukrainian flag
m.get_root().html.add_child(folium.Element('<style> .leaflet-attribution-flag { display: none !important; } </style>'))

#Add ward boundaries to map
functions.ward(dataframe=gdf, fields_name="WARD_NAME", aliases="Ward", map=m)

# Fit the map to the bounds of Cape Town
m.fit_bounds([[-34.35834, 18.30722], [-33.471276, 19.005338]])

match option:
    case "Fire Stations":
        #add fire stations to map
        functions.facilities(dataframe=fire_stations_df, fields_name="FIRE_STN_N",
                             aliases="Fire Station Name:", map=m)
    case "Healthcare Facilities":
        #add healthcare facilities to map
        functions.facilities(dataframe=health_df,fields_name="NAME",
                             aliases="Facility Name:",map=m)

#display map
st_folium(m,width=700, height=500)