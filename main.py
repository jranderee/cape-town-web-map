from pathlib import Path
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import functions


@st.cache_data
def load_shapefile(file_path):
    return gpd.read_file(file_path)

#read shapefiles for air pollution risk
apr2023_df = load_shapefile("Web map data/Air pollution risk/2023/2023_air_pollution_risk.shp")
apr2022_df = load_shapefile("Web map data/Air pollution risk/2022/2022_air_pollution_risk.shp")
apr2021_df = load_shapefile("Web map data/Air pollution risk/2021/2021_Air_pollution_risk.shp")
apr2020_df = load_shapefile("Web map data/Air pollution risk/2020/2020_air_pollution_risk.shp")
apr2019_df = load_shapefile("Web map data/Air pollution risk/2019/2019_air_pollution_risk.shp")

#Read shapefile for monitoring stations
ms_df = load_shapefile("Web map data/Air pollution monitoring stations/CT_air_pollution_stations.shp")

#Read shapefile for SVI
svi_df = load_shapefile("Web map data/SVI/SVI_export.shp")

#Create streamlit title
st.title("Cape Town Air Pollution & Social Vulnerability Index")

option = st.selectbox(
    "Choose an option:",
    ["Air pollution risk 2023","Air pollution risk 2022","Air pollution risk 2021",
     "Air pollution risk 2020","Air pollution risk 2019",
     "Monitoring stations", "Social vulnerability index"]
)

#Create folium map of cape town
m = folium.Map(location=[-33.9249, 18.4241], zoom_start=9, tiles="CartoDB positron")

# Inject CSS to hide the Ukrainian flag
m.get_root().html.add_child(folium.Element('<style> .leaflet-attribution-flag { display: none !important; } </style>'))


# Fit the map to the bounds of Cape Town
m.fit_bounds([[-34.35834, 18.30722], [-33.471276, 19.005338]])

match option:
    case "Air pollution risk 2023":
        #add air pollution risk to map
        functions.air_pollution_risk(dataframe=apr2023_df, data_name="Combined_2",
                                     data_aliases="Air pollution risk:", map=m)
    case "Air pollution risk 2022":
        #add air pollution risk to map
        functions.air_pollution_risk(dataframe=apr2022_df, data_name="Combined_2",
                                     data_aliases="Air pollution risk:", map=m)
    case "Air pollution risk 2021":
        #add air pollution risk to map
        functions.air_pollution_risk(dataframe=apr2021_df, data_name="Combined_2",
                                     data_aliases="Air pollution risk:", map=m)
    case "Air pollution risk 2020":
        #add air pollution risk to map
        functions.air_pollution_risk(dataframe=apr2020_df, data_name="Combined_2",
                                     data_aliases="Air pollution risk:", map=m)
    case "Air pollution risk 2019":
        #add air pollution risk to map
        functions.air_pollution_risk(dataframe=apr2019_df, data_name="Combined_v",
                                     data_aliases="Air pollution risk:", map=m)
    case "Monitoring stations":
        #add monitoring stations to map
        functions.points(dataframe=ms_df, fields_name="Name",
                         aliases="Monitoring station:", map=m)
    case "Social vulnerability index":
        # Add social vulnerability index to map
        functions.social_vul_index(dataframe=svi_df, data_name="SVI",
                                   data_alias="Social vulnerability index: ", map=m, ward_column="WARD_NAME", ward_alias="Ward:")


#display map
st_folium(m, width=700, height=500)