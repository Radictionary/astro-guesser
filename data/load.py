import pandas as pd
import os
import json

folder_path = './parquet'
# folder_path = "WRONG"
parquet_files = [file for file in os.listdir(folder_path) if file.endswith('.parquet')]
total = 0

dataframes = []
for file in parquet_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_parquet(file_path)
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Now you can work with the combined dataframe
# For example, you can print the first few rows
print(combined_df.head())

# Create a new folder to store the images
output_folder = './processed'
os.makedirs(output_folder, exist_ok=True)
# delete all files in the folder
for file in os.listdir(output_folder):
    file_path = os.path.join(output_folder, file)
    os.remove(file_path)

# 0  {'bytes': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHD...  Blow-up of area around GRB 980425: This is an ...  heic0003c  Blow-up of area around GRB 980425  ...      0   False                          None                  None

def get_string_distance(distance_string):
    distance_without_cofactor = float(distance_string.split()[0])
    # million & billion
    if "million" in distance_string:
        return distance_without_cofactor * 1e6
    elif "billion" in distance_string:
        return distance_without_cofactor * 1e9
    else:
        return distance_without_cofactor

def process_row(index, row):
    print(row, row['image'].keys())
    # Get the image data from the dataframe
    image_data = row['image']['bytes']

    hours, minutes, seconds = row['Position (RA)'].split()
    # to ints
    hours, minutes, seconds = int(hours), int(minutes), float(seconds)
    # to degrees
    ra = hours + minutes/60 + seconds/3600

    distance_string = row['Distance']
    # skip redshift values
    if "z=" in distance_string:
        raise ValueError("Redshift values are not supported")
    distance = get_string_distance(distance_string)

    # Generate a unique filename for the image
    image_filename = f'image_{index}.png'
    
    json_string = {
        "name": row['Name'],
        "title": row['title'],
        "ra": ra,
        "distance": distance,
        "image_filename": image_filename,
    }
    
    # Write the image data to the output folder
    image_path = os.path.join(output_folder, image_filename)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    
    # write json file to json folder
    json_filename = f'json_{index}.json'
    json_path = os.path.join(output_folder, json_filename)
    with open(json_path, 'w') as json_file:
        json.dump(json_string, json_file, indent=2)

# Iterate over each row in the combined dataframe
for index, row in combined_df.iterrows():
    if total <= 15:
        try:
            process_row(index, row)
            total += 1
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue