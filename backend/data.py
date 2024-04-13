"""
    This script is responsible for loading the data from the processed folder. It contains the following functions:
    - data_exists(number): checks if a json file exists for a given number
    - load_json(index): loads the json file for a given index
    - random_valid_index(): returns a random index for which a json file exists
    - get_random_data(): returns the data for a random index

    The script also contains a main block that demonstrates the usage of the functions.
"""

import os
import random
import json

# loop through all files in the ./processed folder

folder_path = "./processed"
max_number = float('-inf')

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        try:
            number = float(''.join(c for c in filename if c.isnumeric()))
            max_number = max(max_number, number)
        except ValueError:
            pass

def data_exists(number):
    return os.path.isfile(os.path.join(folder_path, f"json_{number}.json"))

def load_json(index):
    if not data_exists(index):
        return None
    with open(os.path.join(folder_path, f"json_{index}.json"), "r") as f:
        return json.loads(f.read())

def random_valid_index():
    random_number = random.randint(1, max_number)
    while not data_exists(random_number):
        random_number = random.randint(1, max_number)
    return random_number

def get_random_data():
    return load_json(random_valid_index())

if __name__ == "__main__":
    print("Maximum index:", max_number)
    print("Data exists for 1?", data_exists(1))
    print("Data exists for 100?", data_exists(100))
