# To install Python in PowerShell terminal, just type "python" and then install
# After installation, restart the terminal
# Install required Python libraries with: pip install pystac_client rasterio
# Install also: pip install pystac-client planetary-computer odc-stac matplotlib
# Install also: pip install pystac-client planetary-computer rioxarray matplotlib

import matplotlib.pyplot as plt
import planetary_computer as pc
import pystac_client
import rioxarray

# Open the STAC API
stac = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=pc.sign_inplace
)

# Define a search query
search = stac.search(
    collections=["landsat-c2-l2"],
    bbox=[6.207275, 45.567910, 10.755615, 47.680183],  # [min_lon, min_lat, max_lon, max_lat]
    datetime="2020-12-01T10:00:00Z/2020-12-31T14:00:00Z",
    query={"eo:cloud_cover": {"lt": 20}},  # Filter for less than 20% cloud cover
    limit=20  # Fetch up to 20 items
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
    # Get the Blue asset
    blue_asset = item.assets.get('green')

    if blue_asset is not None:
        # Sign the asset's href
        signed_href = pc.sign(blue_asset.href)

        # Open the asset with rioxarray
        da = rioxarray.open_rasterio(signed_href)

        # Display the image
        plt.figure(figsize=(10, 10))
        plt.imshow(da.squeeze(), cmap='Greens')
        plt.show()
        break
else:
    print("None of the items have a 'green' asset")


