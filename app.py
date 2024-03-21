# Import necessary modules
import os
import json
import requests
from flask import Flask, render_template_string, jsonify, request
from resorts import resorts

# Import functions from other files
from main import fetch_resort_data_sequentially, process_resort_data, sort_resorts
from save_data import save_resort_data  # Updated import statement

# Create Flask app
app = Flask(__name__, static_url_path='', static_folder='.')

# Home route
@app.route('/')
def home():
    with open('index.html', 'r') as file:
        html_content = file.read()
    return render_template_string(html_content)

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
    # Check if resort data already exists to avoid redundant fetching
    try:
        with open('resort_data.json', 'r') as file:
            resort_data = json.load(file)
            print("Resort data loaded from file.")
            return resort_data
    except FileNotFoundError:
        print("Resort data file not found. Fetching and processing resort data...")
        resort_data = fetch_and_process_resort_data()
        return resort_data

# Helper function to fetch and process resort data
def fetch_and_process_resort_data():
    # Fetch resort data concurrently
    resort_data = fetch_resort_data_sequentially(resorts)

    # Check if resort data is None
    if resort_data is None:
        return None

    # Process the resort data
    processed_data = process_resort_data(resort_data)

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

    # Save resort data to resort_data.json
    save_resort_data(resort_data_list)

    return resort_data_list

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use port provided by Heroku or default to 5000
    app.run(host="0.0.0.0", port=port)
