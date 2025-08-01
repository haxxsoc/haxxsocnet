import geopandas as gpd
import matplotlib.pyplot as plt

# Load the shapefile for South African provinces
# You can download a shapefile from a reliable source or use a built-in dataset if available
shapefile_path = 'afrgeo.shp'
gdf = gpd.read_file(shapefile_path)

# Plot the provinces
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='lightblue', edgecolor='black')

# Add titles and labels
ax.set_title('Provinces of South Africa', fontsize=15)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)

# Show the plot
plt.show()
