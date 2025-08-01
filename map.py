import folium
'''
# Create a map centered at Durban, South Africa
m = folium.Map(location=[-29.8587, 31.0218], zoom_start=12)

# Add a marker at Durban
folium.Marker(
    location=[-29.8587, 31.0218],
    popup='Durban, South Africa',
    icon=folium.Icon(icon='info-sign')
).add_to(m)
'''
import pandas
import requests
state_geo = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
state_data = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)

m = folium.Map(location=[-28.4793, 24.6727], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(m)

folium.LayerControl().add_to(m)

m

# Save the map to an HTML file
m.save('map.html')


'''''
import geopandas as gpd
import matplotlib.pyplot as plt

# Load a shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot the map
world.plot()
plt.show()
'''
'''
import plotly.express as px

# Load a dataset with geographical information
df = px.data.gapminder().query("year == 2025")

# Create a choropleth map
fig = px.choropleth(df, locations="iso_alpha",
                    color="lifeExp",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma)

fig.show()
'''