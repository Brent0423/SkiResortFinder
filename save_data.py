import json

def save_resort_data(resort_data):
    with open('resort_data.json', 'w') as file:
        json.dump(resort_data, file, indent=4)
    print("Resort data saved successfully.")
