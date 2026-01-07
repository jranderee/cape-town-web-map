import folium



def ward(dataframe, fields_name, aliases, map):
    """Loads ward boundaries onto map"""
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
        zoom_on_click=True,
    ).add_to(map)



def facilities(dataframe, fields_name, aliases, map):
    """Loads data onto map"""
    def style_function(feature):
        """Creates custom marker for facility locations"""
        props = feature.get('properties')
        markup = f"""
            <a href="{props.get('url')}">
                <div style="font-size: 0.8em;">
                <div style="width: 10px;
                            height: 10px;
                            border: 1px solid black;
                            border-radius: 5px;
                            background-color: red;">
                </div>
            </div>
            </a>
        """
        return {"html": markup}
    folium.GeoJson(
        dataframe,
        tooltip=folium.GeoJsonTooltip(
            fields=[fields_name],
            aliases=[aliases],
            localize=True
        ),
        style_function=style_function,
        marker=folium.Marker(icon=folium.DivIcon())
    ).add_to(map)