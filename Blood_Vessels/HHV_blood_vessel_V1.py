"""
Created on Mon Jun 17 15:55:12 2024

@author: heino
"""
import time
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import shape
import json
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
import seaborn as sns


# Recording how long this takes to run
start_time = time.time()

def geojson_from_folder(folder_path):
    geojson_files = []
    items = os.listdir(folder_path)
    for item in items:
        if item.endswith('.geojson'):
            geojson_files.append(folder_path+item)
    return geojson_files


def load_geojson(geojson_path):
    with open(geojson_path) as f:
        data = json.load(f)
    return data


def validate_geometries(data):
    for feature in data['features']:
        geom = shape(feature['geometry'])
        if not geom.is_valid:
            print(f"Invalid geometry found: {feature['properties']}")
            # Attempt to fix invalid geometries
            feature['geometry'] = geom.buffer(0)


def rotate_point(x, y, theta):
    theta_rad = math.radians(theta)
    x_new = x * math.cos(theta_rad) - y * math.sin(theta_rad)
    y_new = x * math.sin(theta_rad) + y * math.cos(theta_rad)
    return x_new, y_new


def rotate_shape(points, theta):
    return [rotate_point(x, y, theta) for x, y in points]


def plot_with_geopandas(gdf):
    plt.figure(figsize=(10, 10), dpi=300)
    gdf.plot()
    plt.show()

geojson_folder = r"C:/Users/heino/Desktop/Problems/blood_vessel/"

# Enter the path to your folder with geojson files
geojson_paths = geojson_from_folder(geojson_folder)

# Enter the names of annotation classes you want measured
classifications_to_measure = ["Orthog Vessel",
                              "Perp Vessel",
                              "PVS",
                              #"Gray Matter",
                              #"White Matter"
                              ]

# This will check 180 degrees of the shape at 10 degree intervals
angles_to_check = list(range(0, 180, 10))
# Creating a dictionary to later store values in
shape_dictionary = {"Image_name": [], "Class": [], "Min Width": []}

for geojson_path in geojson_paths:
    geojson_data = load_geojson(geojson_path)
    validate_geometries(geojson_data)

    # Create a GeoDataFrame from the GeoJSON data
    gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

    # Check for and handle missing or infinite values
    gdf = gdf.replace([float('inf'), float('-inf')], float('nan'))
    gdf = gdf.dropna()

    # Plotting the whole set of annotations
    #plot_with_geopandas(gdf.iloc[0:-1, :])

    # Extracting classifications and shapes from the GeoDataFrame
    classifications = gdf["classification"]
    shapes = gdf["geometry"]

    for i in range(len(shapes)):
    #for i in range(500):
        caliper_measurements = []

        if classifications[i]["name"] in classifications_to_measure:

            shape_coords = shapes[i].coords

            # For each angle requested earlier, set the shape to that angle, and measure x min and x max
            for theta in angles_to_check:
                rotated_shape_coords1 = rotate_shape(shape_coords[:-1], theta)
                rotated_x, rotated_y = zip(*rotated_shape_coords1)

                min_x_bound = min(rotated_x)
                max_x_bound = max(rotated_x)
                width_x_bound = max_x_bound - min_x_bound
                caliper_measurements.append(width_x_bound)

            # Commented out code here is to demo displaying a shape and the width vs angle
            #plot_with_geopandas(gdf.iloc[i:i+1,:]) # plotting the shape
            #plt.plot(angles_to_check, caliper_measurements) # plotting how the capliper measurement changes with the angle
            #plt.show()

            min_caliper = min(caliper_measurements)


            image_name = geojson_path.split("/")[-1]

            shape_dictionary["Image_name"].append(image_name)
            shape_dictionary["Class"].append(classifications[i]["name"])
            shape_dictionary["Min Width"].append(min_caliper)

df = pd.DataFrame(shape_dictionary)
df.to_csv(geojson_folder+"results.csv")

sns.boxplot(x=df["Class"], y=df["Min Width"], palette="RdPu")
sns.swarmplot(x=df["Class"], y=df["Min Width"], size=1, color="black")
plt.ylim(0,300)
plt.show()


# End the timer
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")