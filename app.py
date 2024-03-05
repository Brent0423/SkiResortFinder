# Import necessary modules
import os
import json
import requests
from flask import Flask, render_template, jsonify, request
from resorts import resorts

# Import functions from other files
from main import fetch_resort_data_sequentially, process_resort_data, sort_resorts  # Updated import statement
from save_data import save_resort_data  # Updated import statement

# Create Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    # Use the predefined list of resorts from the resorts module
    resort_list = resorts

    # Fetch resort data sequentially for the predefined list of resorts
    raw_data = fetch_resort_data_sequentially(resorts)
    print("Fetching resort data sequentially...")

    # Check if raw data is None
    if raw_data is None:
        print("Error: Unable to fetch resort data")
        return "Error: Unable to fetch resort data", 500

    # Process the resort data
    processed_data = process_resort_data(raw_data)
    print("Processing resort data...")

    # Check if processed data is None
    if processed_data is None:
        print("Error: Unable to process resort data")
        return "Error: Unable to process resort data", 500

    # Sort the resorts
    rankings = sort_resorts(processed_data)
    print("Sorting resorts...")

    # Check if rankings is None
    if rankings is None:
        print("Error: Unable to sort resorts")
        return "Error: Unable to sort resorts", 500

    # Render the index.html template with the data and enumerate function
    return render_template('index.html', data=rankings, enumerate=enumerate)

# Resorts API route
@app.route('/api/resorts')
def resorts_api():
    # Load resort data
    resort_data = load_resort_data()
    print("Loading resort data...")

    # Check if resort data is None
    if resort_data is None:
        print("Unable to load resort data")
        return jsonify({"error": "Unable to load resort data"}), 500

    # Check if resort data is empty
    if not resort_data:
        print("No resort data available")
        return jsonify({"error": "No resort data available"}), 404

    # Return the resort data as JSON
    return jsonify(resort_data)

# Search Resort API route
@app.route('/api/search', methods=['GET'])
def search_resort():
    # Get the resort name from the request arguments
    resort = request.args.get('resort', default='Jackson Hole', type=str)
    print(f"Searching for resort: {resort}")

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
        print("Resort data file found")
        # Open the file and load the JSON data
        with open('resort_data.json', 'r') as f:
            return json.load(f)
    else:
        print("Resort data file not found, fetching and processing resort data...")
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

    # Convert the sorted resorts to a list of dictionaries including the region
    resort_data_list = [{'name': name, 'score': score, 'region': processed_data[name]['region']} for name, score in sorted_resorts]

    # Ensure each resort data is correctly added to the list
    if not all(resort['name'] for resort in resort_data_list):
        return None  # Return None if any resort data is missing or incorrect

    return resort_data_list

# New endpoint to trigger sequential data fetching and logging
@app.route('/api/sequential-fetch')
def fetch_resorts_data():
    print("Starting sequential data fetching for resorts...")
    for resort in resorts:
        print(f"Fetching data for {resort}...")
        fetch_resort_data_sequentially([resort])
    return jsonify({"message": "Data fetching initiated for all resorts."})

# Run the Flask app if this file is executed directly.
if __name__ == '__main__':
    app.run(debug=False)
