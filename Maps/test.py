import osmnx as ox
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd

# 1. Define your location (Lat, Lon)
lat, lon = 28.6139, 77.2090

tags = {
    "station": "subway",
    "public_transport": "station",
    "railway": "subway_entrance"
}

# 2. Get the features (raw data in Lat/Lon degrees)
nearest = ox.features.features_from_point(
    (lat, lon),
    tags=tags,
    dist=1000
)

# 3. Project the data to a local system (meters) for accurate measurement
# OSMnx has a helper to automatically find the right UTM zone for this location
nearest_proj = ox.projection.project_gdf(nearest)

# 4. Create a geometry for your search point and project it to the same system
# Note: Shapely expects (Longitude, Latitude) order
user_point = Point(lon, lat)
user_point_proj = gpd.GeoSeries([user_point], crs="EPSG:4326").to_crs(nearest_proj.crs).iloc[0]

# 5. Calculate distance in meters, then convert to kilometers
nearest['distance_km'] = nearest_proj.distance(user_point_proj) / 1000

# 6. Sort by closest and print specific columns
print(nearest[['name', 'distance_km']].sort_values(by='distance_km').head())
df = pd.DataFrame(nearest)
df.to_csv("test.csv")
