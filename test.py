import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd
from pyproj import Proj, Transformer

st.title("Cape Town Wards Map with Fire Stations")

# Load data
shapefile_path = "Wards/Wards.shp"
gdf = gpd.read_file(shapefile_path)

csv_path = "Fire_Stations.csv"
points_df = pd.read_csv(csv_path)

# Display original coordinates for debugging
st.write("### Original Fire Station Coordinates (UTM)")
st.write(f"X range: {points_df['X'].min():.2f} to {points_df['X'].max():.2f}")
st.write(f"Y range: {points_df['Y'].min():.2f} to {points_df['Y'].max():.2f}")

# Determine UTM zone for Cape Town (Zone 34S for South Africa)
# Cape Town uses UTM Zone 34S (EPSG:32734) or 34H
# Let's detect the correct CRS
# Try WGS84 UTM Zone 34S (southern hemisphere)
utm_zone = 34  # Cape Town is in UTM zone 34
south_hemisphere = True  # Since Y values are negative

# Create transformer - UTM to WGS84 (lat/lon)
# Based on the coordinates, this appears to be UTM Zone 34S (EPSG:32734)
# But let's check if it might be Hartebeesthoek94 / Lo31 (EPSG:2053)
try:
    # Option 1: Try UTM Zone 34S (WGS84)
    transformer = Transformer.from_crs("EPSG:32734", "EPSG:4326", always_xy=True)

    # Convert coordinates
    points_df['lon'], points_df['lat'] = transformer.transform(
        points_df['X'].values,
        points_df['Y'].values
    )

    # Check if conversion looks reasonable
    st.write("### Converted Coordinates (WGS84)")
    st.write(f"Latitude range: {points_df['lat'].min():.6f} to {points_df['lat'].max():.6f}")
    st.write(f"Longitude range: {points_df['lon'].min():.6f} to {points_df['lon'].max():.6f}")

except Exception as e:
    st.warning(f"UTM Zone 34S conversion failed: {e}")

    # Option 2: Try Hartebeesthoek94 / Lo31 (common for South Africa)
    try:
        transformer = Transformer.from_crs("EPSG:2053", "EPSG:4326", always_xy=True)
        points_df['lon'], points_df['lat'] = transformer.transform(
            points_df['X'].values,
            points_df['Y'].values
        )
        st.success("Used Hartebeesthoek94 / Lo31 (EPSG:2053) projection")
    except Exception as e2:
        st.error(f"Both conversions failed: {e2}")
        # Fallback: Use approximate conversion (less accurate)
        st.warning("Using approximate conversion - results may be offset")
        # These are rough offsets - will get stations in Cape Town area but not exact
        points_df['lat'] = -33.9 + (points_df['Y'] + 4000000) / 100000
        points_df['lon'] = 18.4 + (points_df['X'] - 2050000) / 100000

# Display converted coordinates
st.write("### Sample Converted Stations")
st.dataframe(points_df[['FIRE_STN_NAME', 'X', 'Y', 'lat', 'lon']].head())

# Create map centered on Cape Town
m = folium.Map(location=[-33.9249, 18.4241], zoom_start=10, tiles="CartoDB positron")

# Add wards
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

# Add fire station markers
for index, row in points_df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"""
        <div style='font-family: Arial; font-size: 12px;'>
            <b>{row['FIRE_STN_NAME']}</b><br>
            Code: {row['FIRE_STN_CODE']}<br>
            Type: {row['FIRE_STN_CLASS']}<br>
            UTM X: {row['X']:.1f}<br>
            UTM Y: {row['Y']:.1f}
        </div>
        """,
        tooltip=row['FIRE_STN_NAME'],
        icon=folium.Icon(color="red", icon="fire", prefix="fa")
    ).add_to(m)

# Add a test marker at Cape Town center
folium.Marker(
    location=[-33.9249, 18.4241],
    popup="Cape Town City Center",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(m)

# Display map
st_folium(m, width=700, height=500)

# Show all stations in a table
with st.expander("View All Fire Station Locations"):
    st.dataframe(points_df[['FIRE_STN_NAME', 'lat', 'lon']])