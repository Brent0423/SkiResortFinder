import os
import time
import requests
from dotenv import load_dotenv
from resorts import resorts

# Load environment variables
load_dotenv(dotenv_path='rapid.env')

# Access the API_KEY environment variable
api_key = os.getenv("API_KEY")

# Initialize a session for connection reuse
session = requests.Session()
session.headers.update({
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
})

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
        print(f"Warning: Measurement format for '{measurement}' not recognized.")
        return 0

def process_resort_data(resort_data):
    # Processes the raw resort data and extracts relevant snow condition information.
    processed_data = {}
    for resort, data in resort_data.items():
        snow_data = data.get('imperial', {})
        processed_data[resort] = {
            'topSnowDepth': parse_depth(snow_data.get('topSnowDepth', '0in')),
            'botSnowDepth': parse_depth(snow_data.get('botSnowDepth', '0in')),
            'freshSnowfall': parse_depth(snow_data.get('freshSnowfall', '0in')),
        }
    return processed_data

def fetch_resort_data_sequentially(resorts, delay=2):
    # Fetches resort data using sequential requests with delay.
    base_url = "https://ski-resort-forecast.p.rapidapi.com/{}/snowConditions"
    resort_data = {}
    for resort in resorts:
        try:
            formatted_resort_name = resort.replace(" ", "%20")
            url = base_url.format(formatted_resort_name)
            response = session.get(url, timeout=5)  # Use session for requests
            response.raise_for_status()
            resort_data[resort] = response.json()
            print(f"Data fetched for {resort}.")
        except requests.exceptions.RequestException as e:
            print(f"Request error for {resort}: {e}")
            resort_data[resort] = None  # Handle errors by setting data to None
        time.sleep(delay)  # Wait for specified delay to avoid hitting rate limits
    return resort_data

def sort_resorts(processed_data):
    # Ranks resorts based on normalized snow condition scores.
    if not processed_data:
        return []
    max_values = {
        'topSnowDepth': max(resort_data['topSnowDepth'] for resort_data in processed_data.values() if resort_data['topSnowDepth']),
        'botSnowDepth': max(resort_data['botSnowDepth'] for resort_data in processed_data.values() if resort_data['botSnowDepth']),
        'freshSnowfall': max(resort_data['freshSnowfall'] for resort_data in processed_data.values() if resort_data['freshSnowfall']),
    }

    for resort_data in processed_data.values():
        for key, value in max_values.items():
            resort_data[key] /= value if value != 0 else 1  # Prevent division by zero

    total_scores = {resort: sum(resort_data.values()) for resort, resort_data in processed_data.items()}
    return sorted(total_scores.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    print("Starting to fetch resort data...")
    raw_data = fetch_resort_data_sequentially(resorts)
    processed_data = process_resort_data(raw_data)
    top_resorts = sort_resorts(processed_data)
    print("\nTop Resorts based on snow conditions:")
    for resort, score in top_resorts:
        print(f"{resort}: Score {score}")
