import pydeck as pdk

import os
from dash import Dash, html
import dash_deck
mapbox_api_token = "pk.eyJ1IjoicHl0aG9uYmFiYSIsImEiOiJja3U5aTE2YWcwNzZjMzJsOXFnZXpjcnE5In0.1dv4v5tP4VYOxNrvMmeL4Q"


TERRAIN_IMAGE = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

# Define how to parse elevation tiles
ELEVATION_DECODER = {"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768}

SURFACE_IMAGE = f"https://api.mapbox.com/v4/mapbox.satellite/{{z}}/{{x}}/{{y}}@2x.png?access_token={mapbox_api_token}"

terrain_layer = pdk.Layer(
    "TerrainLayer", elevation_decoder=ELEVATION_DECODER, texture=SURFACE_IMAGE, elevation_data=TERRAIN_IMAGE
)

geojson = pdk.Layer(
    "GeoJsonLayer",
    'https://raw.githubusercontent.com/muntakim1/flood-prone-gis/refs/heads/main/data/filtered.geojson',	
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.elevation / 20",
    get_fill_color="[135, 206, 235]",
    get_line_color=[135, 206, 235],
)
view_state = pdk.ViewState(latitude=23.232100, longitude=90.663078, zoom=11.5, bearing=10, pitch=45)

r = pdk.Deck([terrain_layer,geojson], initial_view_state=view_state)
deck_component = dash_deck.DeckGL(r.to_json(), id="deck-gl", mapboxKey=mapbox_api_token)

app = Dash(__name__)
app.layout = html.Div(deck_component)

if __name__ == "__main__":
    app.run_server(debug=True)