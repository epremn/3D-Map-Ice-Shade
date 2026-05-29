import numpy as np
import plotly.graph_objects as go
import xarray as xr
import webbrowser
import os

url = 'https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO2022/15s/15s_surface_elev_netcdf/ETOPO_2022_v1_15s_N45W015_surface.nc'
xrds = xr.open_dataset(url)

# Select an interesting region – here we use the Strait of Gibraltar
xrds_sub = xrds.sel(lat=slice(35, 37), lon=slice(-6, -4))

# Extract the data arrays from the xarray object
lat = xrds_sub['lat'].values   # 1D array of latitudes
lon = xrds_sub['lon'].values   # 1D array of longitudes
z   = xrds_sub['z'].values     # 2D array of relief values

# Create a 2D meshgrid matching the spatial layout of your data
lon2d, lat2d = np.meshgrid(lon, lat)

# Define a custom diverging colourscale that emphasises the transition at sea level.
# Compute the normalised position of sea level (0 m) within the data range.
zmin, zmax = z.min(), z.max()
mid = (0 - zmin) / (zmax - zmin)
# The colours below sea level (blue hues) and above (green to brown) are defined.
custom_colorscale = [
    [0.0, 'navy'],          # Deepest water
    [mid, 'deepskyblue'],    # Transition within the water column
    [mid, 'lightgreen'],     # Land just above sea level
    [1.0, 'saddlebrown']     # Highest elevations
]

# Create the interactive 3D surface plot with enhanced lighting and contours
fig = go.Figure(data=[go.Surface(
    x=lon2d,
    y=lat2d,
    z=z,
    colorscale=custom_colorscale,
    colorbar=dict(title='Relief (m)'),
    lighting=dict(ambient=0.8, diffuse=0.5, specular=0.2, roughness=0.9),
    contours={
        "z": {
            "show": True,
            "usecolormap": True,
            "highlightcolor": "limegreen",
            "project": {"z": True}
        }
    }
)])

# Update the layout to improve the visual appeal
fig.update_layout(
    title=dict(
        text="3D Bathymetry and Topography: Strait of Gibraltar",
        x=0.5,
        xanchor='center',
        font=dict(size=24)
    ),
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Relief (m)',
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.7)),
        aspectratio=dict(x=1, y=1, z=0.2)
    ),
    width=900,   # Increase width
    height=600    # Increase height
)

# Display the interactive plot – you can zoom, pan and rotate to examine details
fig.show() 

# I need to include this line, and the cell below, to make the plot display in this jupyter book.
# This is not neccessary in a jupyter notebook or your python script - just uncomment the fig.show() line above.
fig.write_html("interactive_plot_relief.html")

# Open the HTML file in the default browser
html_file = os.path.abspath("interactive_plot_relief.html")
webbrowser.open('file://' + html_file)