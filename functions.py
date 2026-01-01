import folium


def ward(dataframe, fields_name, aliases, map):
    folium.GeoJson(
        dataframe,
        style_function=lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.1
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[fields_name],
            aliases=[aliases],
            localize=True
        ),
        zoom_on_click=True
    ).add_to(map)

def facilities(dataframe, fields_name, aliases, map):
    folium.GeoJson(
        dataframe,
        tooltip=folium.GeoJsonTooltip(
            fields=[fields_name],
            aliases=[aliases],
            localize=True
        )
    ).add_to(map)