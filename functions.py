import folium



def areas(dataframe, fields_name, aliases, map):
    """Loads ward boundaries onto map"""

    def style_function(feature):
        """Defines custom style for facility boundaries and dynamic background"""
        props = feature['properties']

        # Get value from  column specified by fields_name
        value = props.get(fields_name)

        # Default to gray if value is missing or invalid
        if value is None or not isinstance(value, (int, float)):
            fill_color = 'gray'
        else:
            # Numerical color mapping: Scale from 1 (light color) to 10 (dark color)
            if value == 1:
                fill_color = '#f0f921'
            elif value == 2:
                fill_color = '#fdca26'
            elif value == 3:
                fill_color = '#fb9f3a'
            elif value == 4:
                fill_color = '#ed7953'
            elif value == 5:
                fill_color = '#d8576b'
            elif value == 6:
                fill_color = '#bd3786'
            elif value == 7:
                fill_color = '#9c179e'
            elif value == 8:
                fill_color = '#7201a8'
            elif value == 9:
                fill_color = '#46039f'
            elif value == 10:
                fill_color = '#0d0887'
            else:
                fill_color = 'gray'

        return {
            'color': 'black',  # Boundary line color
            'weight': 2,  # Line thickness
            'opacity': 1,  # Line opacity
            'fillColor': fill_color,  # Dynamic fill color based on the column
            'fillOpacity': 0.5  # Fill transparency
        }
    folium.GeoJson(
        dataframe,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=[fields_name],
            aliases=[aliases],
            localize=True
        ),
        zoom_on_click=True,
    ).add_to(map)



def points(dataframe, fields_name, aliases, map):
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