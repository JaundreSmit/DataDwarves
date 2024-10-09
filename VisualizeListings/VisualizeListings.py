import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the listings from the Excel file
try:
    listings_df = pd.read_excel('listings.xlsx')
except FileNotFoundError:
    print("Error: listings.xlsx file not found.")
    exit()

# Load the neighborhoods from the GeoJSON file
try:
    neighborhoods_gdf = gpd.read_file('neighbourhoods.geojson')  # Change this to your neighborhoods file
except FileNotFoundError:
    print("Error: neighborhoods.geojson file not found.")
    exit()

# Display the first few rows of the listings DataFrame
print("First few rows of listings DataFrame:")
print(listings_df.head())

# Drop rows with NaN values in latitude or longitude
listings_df = listings_df.dropna(subset=['latitude', 'longitude'])

# Display the DataFrame after dropping NaN values
print("Listings DataFrame after dropping NaN:")
print(listings_df)

# Create a GeoDataFrame from the listings DataFrame
listings_gdf = gpd.GeoDataFrame(
    listings_df, 
    geometry=gpd.points_from_xy(listings_df.longitude, listings_df.latitude),
    crs="EPSG:4326"
)

# Check the number of valid points
num_valid_points = len(listings_gdf)
print(f"Number of valid points in listings GeoDataFrame: {num_valid_points}")

# Create a plot
fig, ax = plt.subplots(figsize=(12, 12))

# Plot the neighborhoods
neighborhoods_gdf.plot(ax=ax, color='lightgrey', edgecolor='black', alpha=0.5, label='Neighborhoods')

# Check if there are valid points to plot
if num_valid_points == 0:
    print("No valid points to plot.")
else:
    # Plot the listings
    listings_gdf.plot(ax=ax, color='red', markersize=10, label='Listings')

    # Set plot title and labels
    ax.set_title('Airbnb Listings in Cape Town with Neighborhoods', fontsize=15)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()
