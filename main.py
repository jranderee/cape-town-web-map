import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd
from shapely.geometry import Point


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

for index, row in points_df.iterrows():
    folium.Marker(
        location=[row["Y"], row["X"]],
        popup=row["FIRE_STN_NAME"],
        tooltip=row["FIRE_STN_NAME"]
    ).add_to(m)

st_folium(m,width=700, height=500)

# DEBUG: Show column names and first few rows
st.write("### CSV Columns:", points_df.columns.tolist())
st.write("### First 5 rows:", points_df.head())