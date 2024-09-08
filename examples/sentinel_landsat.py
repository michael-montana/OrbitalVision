# To install Python in PowerShell terminal, just type "python" and then install
# After installation, restart the terminal
# Install required Python libraries with: pip install pystac_client rasterio
# Install also: pip install pystac-client planetary-computer odc-stac matplotlib
# Install also: pip install pystac-client planetary-computer rioxarray matplotlib

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




# Define the bounding box coordinates
bbox = [138.992157,36.072412,140.640106,37.510815]  # [min_lon, min_lat, max_lon, max_lat]

def display_image(collection, figure_number):
    # Define a search query
    search = stac.search(
        collections=[collection],
        bbox=bbox,
        datetime="2022-12-01T10:00:00Z/2024-12-31T14:00:00Z",
        query={"eo:cloud_cover": {"lt": 20}},  # Filter for less than 20% cloud cover
        limit=40  # Fetch up to 20 items
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
            
            # Display the image in a new figure
            plt.figure(figure_number, figsize=(10, 10))
            plt.imshow(da.squeeze().transpose('y', 'x', 'band'))
            plt.show()
            break
    else:
        print(f"None of the items in the {collection} collection have a 'rendered_preview' asset")

# Display an image for the Sentinel-2 Level-2A collection in figure 1
display_image("sentinel-2-l2a", 1)

# Display an image for the Landsat Collection 2 Level-2 collection in figure 2
display_image("landsat-c2-l2", 2)