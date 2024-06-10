from PIL import Image, ImageFile
import pandas as pd
import os


# Enable the use of large images (~2bil pixel limit by default, these slides are ~2.5bil)
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True
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
    # Create a dictionary of coords to crop tp
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


# Paste the image paths here (order matters)
input_image_paths =[
]
# Paste the csv paths here (order must match the list above)
object_info_paths = [
]


# set the output folder you want the cropped images saved to
output_path_base = "C:/Users/heino/Desktop/Lewy_body_problem/Cropped/"
# set how much space you want around each cropped image

# Loop through each image name and the complimentary csv to that image
for q in range(len(input_image_paths)):
    input_image_path = input_image_paths[q]
    object_info_csv_path = object_info_paths[q]
    # make a dictionary of coordinates to crop
    crop_coordinates_dictionary = dict_of_cords(object_info_csv_path, crop_buffer=30)
    # crop the image at all designated locations, and save to the output path
    crop_image(input_image_path, output_path_base, crop_coordinates_dictionary)
