import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd


shapefile_path = "Wards/Wards.shp"
gdf = gpd.read_file(shapefile_path)

csv_path = "Fire_Stations.csv"
points_df = pd.read_csv(csv_path)

st.title("Cape Town Wards Map")

m = folium.Map(location=[-33.9249, 18.4241], zoom_start=10, tiles="CartoDB positron")

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
        localize=True
    )
).add_to(m)

st_folium(m,width=700, height=500)