# Import necessary modules
import os
import json
import requests
from flask import Flask, render_template, jsonify, request

# Import functions from other files
from main import fetch_resort_data_sequentially, process_resort_data, sort_resorts
from resorts import resorts

# Create Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    # Create an empty list to store test resorts
    test_resorts = []

    # Fetch resort data sequentially
    raw_data = fetch_resort_data_sequentially(test_resorts)

    # Check if raw data is None
    if raw_data is None:
        return "Error: Unable to fetch resort data", 500

    # Process the resort data
    processed_data = process_resort_data(raw_data)

    # Check if processed data is None
    if processed_data is None:
        return "Error: Unable to process resort data", 500

    # Sort the resorts
    rankings = sort_resorts(processed_data)

    # Check if rankings is None
    if rankings is None:
        return "Error: Unable to sort resorts", 500

    # Render the index.html template with the data and enumerate function
    return render_template('index.html', data=rankings, enumerate=enumerate)

# Resorts API route
@app.route('/api/resorts')
def resorts_api():
    # Load resort data
    resort_data = load_resort_data()

    # Check if resort data is None
    if resort_data is None:
        return jsonify([]), 500

    # Return the resort data as JSON
    return jsonify(resort_data)

# Search Resort API route
@app.route('/api/search', methods=['GET'])
def search_resort():
    # Get the resort name from the request arguments
    resort = request.args.get('resort', default='Jackson Hole', type=str)

    # Replace spaces with '%20' in the resort name
    resort = resort.replace(' ', '%20')

    # Create the URL for the API request
    url = f"https://ski-resort-forecast.p.rapidapi.com/{resort}/snowConditions"

    # Set the querystring parameters
    querystring = {"units": "i"}

    # Set the headers for the API request
    headers = {
        "X-RapidAPI-Key": "e4644d7644mshcb7e90e40cf6593p18d651jsnaf7a44aec097",
        "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
    }

    try:
        # Send the API request
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()

        # Return the API response as JSON
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        # Return an error message as JSON
        return jsonify({"error": str(e)}), 500

# Helper function to load resort data
def load_resort_data():
    # Check if the resort_data.json file exists
    if os.path.exists('resort_data.json'):
        # Open the file and load the JSON data
        with open('resort_data.json', 'r') as f:
            return json.load(f)
    else:
        # Fetch and process resort data
        resort_data = fetch_and_process_resort_data()

        # Check if resort data is None
        if resort_data is None:
            return None

        # Save resort data to resort_data.json
        save_resort_data(resort_data)

        # Return the resort data
        return resort_data

# Helper function to fetch and process resort data
def fetch_and_process_resort_data():
    # Fetch resort data sequentially
    raw_data = fetch_resort_data_sequentially(resorts)

    # Check if raw data is None
    if raw_data is None:
        return None

    # Process the resort data
    processed_data = process_resort_data(raw_data)

    # Check if processed data is None
    if processed_data is None:
        return None

    # Sort the resorts
    sorted_resorts = sort_resorts(processed_data)

    # Check if sorted resorts is None
    if sorted_resorts is None:
        return None

    # Convert the sorted resorts to a list of dictionaries
    return [{'name': name, 'score': score} for name, score in sorted_resorts]

# Helper function to save resort data
def save_resort_data(resort_data):
    # Open the resort_data.json file in write mode
    with open('resort_data.json', 'w') as f:
        # Write the resort data as JSON to the file
        json.dump(resort_data, f)

# Run the Flask app if this file is executed directly.
if __name__ == '__main__':
    app.run(debug=False)
