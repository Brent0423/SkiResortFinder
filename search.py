import requests
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from a .env file for secure access to sensitive data
load_dotenv(dotenv_path='rapid.env')

# Retrieve the API key from environment variables for authentication
api_key = os.getenv("API_KEY")

def search_resort(resort_name):
    """
    Searches for snow conditions of a given ski resort by name.

    Parameters:
    resort_name (str): The name of the ski resort to search for.

    Returns:
    dict: The snow conditions data for the specified resort, or None if an error occurs.
    """
    try:
        # Validate input to ensure meaningful search query
        if not resort_name:
            print("Error: Resort name cannot be empty.")
            return None

        # Prepare the resort name for inclusion in the URL by encoding special characters
        encoded_resort_name = quote_plus(resort_name)
        url = f"https://ski-resort-forecast.p.rapidapi.com/{encoded_resort_name}/snowConditions"

        # Set up the request headers with the necessary API credentials
        headers = {
            "X-RapidAPI-Key": api_key,  # Authentication key
            "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"  # API host
        }

        # Execute the GET request to retrieve snow conditions data from the API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure a successful response (2XX status code)

        # Convert the JSON response into a Python dictionary and return it
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        # Log any errors encountered during the request to the console
        print("Error fetching data:", e)
        return None

# Demonstrate the function's usage in a standalone script context
if __name__ == "__main__":
    # Specify the resort name to search for
    search_value = "YourResortName"
    # Attempt to retrieve and print the snow conditions data for the specified resort
    resort_data = search_resort(search_value)
    if resort_data:
        # Successfully retrieved data
        print(resort_data)
    else:
        # Data retrieval failed or no data available
        print("No data found for the specified resort.")

