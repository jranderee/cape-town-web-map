import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

#read shapefile for ward boundaries
shapefile_path = "Wards/Wards.shp"
gdf = gpd.read_file(shapefile_path)

#read shapefile for fire stations
fire_stations_path = "Fire_Stations/Fire_Stations.shp"
fire_statins_df = gpd.read_file(fire_stations_path)

#Read shapefile for healthcare facilities
health_facilities_path = "Health_Care_Facilities/Health_Care_Facilities_(Clinics%2C_Hospitals).shp"
health_df = gpd.read_file(health_facilities_path)

#Create streamlit title
st.title("Cape Town Wards Map")

option = st.selectbox(
    "Choose an option:",
    ["None","Fire Stations", "Healthcare Facilities"]
)


#Create folium map of cape town
m = folium.Map(location=[-33.9249, 18.4241], zoom_start=9, tiles="CartoDB positron")

# Inject CSS to hide the Ukrainian flag
m.get_root().html.add_child(folium.Element('<style> .leaflet-attribution-flag { display: none !important; } </style>'))

#Add ward boundaries to map
folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        "fillColor": "blue",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.1
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["WARD_NAME"],
        aliases=["Ward"],
        localize=True
    )
).add_to(m)

# Fit the map to the bounds of Cape Town
m.fit_bounds([[-34.35834, 18.30722], [-33.471276, 19.005338]])

match option:
    case "Fire Stations":
        #add fire stations to map
        folium.GeoJson(
            fire_statins_df,
            tooltip=folium.GeoJsonTooltip(
                fields=["FIRE_STN_N"],
                aliases=["Fire Station Name:"],
                localize=True
            )
        ).add_to(m)

    case "Healthcare Facilities":
        folium.GeoJson(
            health_df,
            tooltip=folium.GeoJsonTooltip(
                fields=["NAME"],
                aliases=["Facility Name:"],
                localize=True
            )
            ).add_to(m)


#display map
st_folium(m,width=700, height=500)