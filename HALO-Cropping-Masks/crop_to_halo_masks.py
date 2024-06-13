# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:08:07 2024

@author: heino
"""


"""
This code assumes you have 3 folders:
1. A folder with images you want to crop many areas of
2. A folder with CSVs exported from HALO with respect to the images in folder 1
        This code assumes these are named <image_name>.svs_object_Data.csv
3. A folder you want these cropped images saved to 
"""
# if the image data for layers exports one CSV at a time, we may want to use the CSV to call on the image
# Flip it so CSV spits out a predicted image name

from PIL import Image, ImageFile
import pandas as pd
import os


# Enable the use of large images (~2bil pixel limit by default, these slides are ~2.5bil)
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True


# Define functions
def crop_image(input_path,output_path_base, crop_coordinates_dictionary):
    # Open the image
    with Image.open(input_path) as img:

        for i in range(len(crop_coordinates_dictionary)):
            crop_box = crop_coordinates_dictionary[i]
            # Calculate the crop box
            left, upper, right, lower = crop_box

            #calculate the center of object
            center_x = left+right/2
            center_y = upper+lower/2

            # Crop the image around the designated coords
            cropped_img = img.crop((left, upper, right, lower))

            # extract slide name from path
            slide_file_name = input_path.split("/")[-1]
            slide_name = slide_file_name.split(".")[0]

            # save cropped image with slide name and object number
            output_path = output_path_base + slide_name + "_object_" + str(i) + '_x_' + str(round(center_x)) + '_y_' + str(round(center_y)) + '.png'
            cropped_img.save(output_path)

            print(f"Cropped image saved to {output_path}")


def dict_of_cords(object_info_csv, crop_buffer):
    # Create a dictionary of coords to crop to
    df = pd.read_csv(object_info_csv)
    object_ids = df["Object Id"]
    X_mins = df["XMin"]
    X_maxs = df["XMax"]
    Y_mins = df["YMin"]
    Y_maxs = df["YMax"]

    crop_coordinates_dictionary = {}
    # build crop_coords dictionary
    for j in range(len(object_ids)):
        crop_coordinates_dictionary[j] = [X_mins[j] - crop_buffer, Y_mins[j] - crop_buffer, X_maxs[j] + crop_buffer,
                                          Y_maxs[j] + crop_buffer]
    return crop_coordinates_dictionary


def make_list_of_files_in_folder(folder_path):
    list_of_files = []

    if not os.path.isdir(folder_path):
        print("Error: Not a valid directory path.")
        return
    # Get list of files in the directory
    files = os.listdir(folder_path)
    
    # Print each file
    for file in files:
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(os.path.join(folder_path, file)):
            list_of_files.append(file)
    
    return sorted(list_of_files)


def crop_images_in_folder_based_on_object_data(image_folder_path, object_info_path, output_path_base):
    files_in_image_folder = make_list_of_files_in_folder(image_folder_path)
    files_in_object_data_folder = make_list_of_files_in_folder(object_info_path)
    
    predicted_csv_names = []
    for file_in_image_folder in files_in_image_folder:
        predicted_csv_names.append(file_in_image_folder+"_object_Data.csv")
    
    # Check that each image has a matching CSV folder with object data
    for predicted_csv_name in predicted_csv_names:
        if predicted_csv_name not in files_in_object_data_folder:
            print(f"Error: No CSV matching the expected name: {predicted_csv_name}")
            return
    
    # Loop through each image name and the complimentary csv to that image
    for q in range(len(files_in_image_folder)):
        
        # create the full path for the iamge and the CSV
        input_image_path = image_folder_path + files_in_image_folder[q]
        object_info_csv_path = object_info_path + files_in_object_data_folder[q]
        
        # make a dictionary of coordinates to crop to
        crop_coordinates_dictionary = dict_of_cords(object_info_csv_path, crop_buffer=30)
        
        # crop the image at all designated locations, and save to the output path
        crop_image(input_image_path, output_path_base, crop_coordinates_dictionary)
  
        
# Paste the path to your image folder here
image_folder_path = "C:/Users/heino/Desktop/Problems/Lewy_body_problem/Images/"
# Paste the path to your object data folder here
object_info_path = "C:/Users/heino/Desktop/Problems/Lewy_body_problem/ObjectData/"
# Paste the path to the folder you want the cropped images saved to
output_path_base = "C:/Users/heino/Desktop/Problems/Lewy_body_problem/Cropped/"

crop_images_in_folder_based_on_object_data(image_folder_path, object_info_path, output_path_base)