# Import necessary modules
import os
import time
import requests
from dotenv import load_dotenv
from resorts import resorts

# Load environment variables
load_dotenv(dotenv_path='rapid.env')
print("Environment variables loaded.")

# Access the API_KEY environment variable
api_key = os.getenv("API_KEY")
print("API key accessed.")

# Initialize a session for connection reuse
session = requests.Session()
session.headers.update({
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
})
print("Session initialized with headers.")

# Constants
BASE_URL = "https://ski-resort-forecast.p.rapidapi.com/{}/snowConditions"
DELAY_BETWEEN_REQUESTS = 1
print("Constants set.")

def parse_depth(measurement):
    # Parses the snow depth measurement and converts it to inches if necessary.
    if not measurement:  # Handles None or empty string
        return 0
    if measurement.endswith('cm'):
        value_cm = int(measurement.rstrip('cm'))
        value_in = value_cm * 0.393701
        return round(value_in, 2)
    elif measurement.endswith('in'):
        return int(measurement.rstrip('in'))
    else:
        return 0
    print("Snow depth measurement parsed.")

def fetch_resort_data_sequentially(resorts):
    # Fetches resort data using sequential requests with delay.
    if not resorts:
        return None
    resort_data = {}
    for resort in resorts:
        try:
            formatted_resort_name = resort.replace(" ", "%20")
            url = BASE_URL.format(formatted_resort_name)
            response = session.get(url, timeout=5)  # Use session for requests
            if response.status_code == 200:
                data = response.json()
                resort_data[resort] = data
            else:
                resort_data[resort] = None
        except requests.exceptions.RequestException as e:
            resort_data[resort] = None  # Handle errors by setting data to None
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Wait for specified delay to avoid hitting rate limits
    print("Resort data fetched sequentially.")
    return resort_data

def process_resort_data(resort_data):
    if not resort_data:
        return None
    processed_data = {}
    for resort, data in resort_data.items():
        if data is None or 'imperial' not in data:
            continue
        imperial_data = data['imperial']
        # Safely access nested 'region' value
        region = imperial_data.get('basicInfo', {}).get('region', 'N/A')
        processed_data[resort] = {
            'topSnowDepth': parse_depth(imperial_data.get('topSnowDepth', '0in')),
            'botSnowDepth': parse_depth(imperial_data.get('botSnowDepth', '0in')),
            'freshSnowfall': parse_depth(imperial_data.get('freshSnowfall', '0in')),
            'region': region  # Safely extracted region
        }

    # Calculate percentile scores for each snow condition
    for key in ['topSnowDepth', 'botSnowDepth', 'freshSnowfall']:
        values = [float(processed_data[resort][key]) for resort in processed_data if key in processed_data[resort]]
        if values:
            max_value = max(values)
            percentile_scores = {resort: f"{round((value / max_value) * 100, 3)}%" for resort, value in zip(processed_data.keys(), values)}
            for resort in processed_data:
                if key in processed_data[resort]:
                    processed_data[resort][key] = percentile_scores[resort]

    print("Resort data processed.")
    return processed_data

def sort_resorts(processed_data):
    # Ranks resorts based on normalized snow condition scores.
    if not processed_data:
        return []

    total_scores = {resort: sum([float(resort_data[key].rstrip('%')) for key in resort_data if key != 'region']) for resort, resort_data in processed_data.items()}
    max_score = max(total_scores.values())
    normalized_scores = {resort: (score / max_score) * 100 for resort, score in total_scores.items()}
    sorted_resorts = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
    print("Resorts sorted based on normalized snow condition scores.")
    return sorted_resorts

def check_json_file():
    # Check if a JSON file already exists or if data needs to be fetched
    if os.path.exists('resort_data.json'):
        print("JSON file already exists.")
        return True
    else:
        print("JSON file does not exist. Data needs to be fetched.")
        return False

check_json_file()
