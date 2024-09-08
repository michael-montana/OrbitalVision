"""
This script provides instructions for setting up the Python environment and installing required libraries.

To install Python in PowerShell terminal, just type "python" and follow the installation instructions.
After installation, restart the terminal.

Install required Python libraries with:
    pip install pystac_client rasterio

Additionally, install:
    pip install pystac-client planetary-computer odc-stac matplotlib
    pip install pystac-client planetary-computer rioxarray matplotlib

Author: Michael Montana
Link: https://github.com/michael-montana
"""

import matplotlib.pyplot as plt
import planetary_computer as pc
import pystac_client
import rioxarray
import warnings
from rasterio.errors import NotGeoreferencedWarning

# Suppress the NotGeoreferencedWarning
warnings.filterwarnings('ignore', category=NotGeoreferencedWarning)

# Open the STAC API
stac = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace
)

# Define a search query
search = stac.search(
    collections=["sentinel-1-rtc"],
    bbox=[139.780726,35.625192,139.806798,35.644672],  # [min_lon, min_lat, max_lon, max_lat]
    datetime="2022-12-01T10:00:00Z/2024-08-28T23:00:00Z",
    query={},  # Filter for less than 20% cloud cover
    limit=40  # Fetch up to 40 items
)

# Get the items from the search results
items = search.item_collection()

# Check if there are any items
if len(items) > 0:
    # Print the asset keys of the first item
    print("Assets of the first item:", list(items[0].assets.keys()))
else:
    print("No items found")

# Iterate over the items
for item in items:
    # Get the Rendered Preview asset
    preview_asset = item.assets.get('rendered_preview')

    if preview_asset is not None:
        # Sign the asset's href
        signed_href = pc.sign(preview_asset.href)

        # Open the asset with rioxarray
        da = rioxarray.open_rasterio(signed_href)
        
        # Select the first three channels
        da = da.sel(band=slice(1, 3))
        
        # Display the image
        # Create a figure with a specific size
        plt.figure(figsize=(10, 10))

        # Display the image
        plt.imshow(da.squeeze().transpose('y', 'x', 'band'))

        # Add axis labels
        plt.xlabel("Longitude", fontsize=14)
        plt.ylabel("Latitude", fontsize=14)

        # Add a grid
        plt.grid(False)

        # Show the plot
        plt.show()
        break
else:
    print("None of the items have a 'rendered_preview' asset")