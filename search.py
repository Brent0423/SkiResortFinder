import requests
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from 'rapid.env' file
load_dotenv(dotenv_path='rapid.env')

# Access the API_KEY environment variable
api_key = os.getenv("API_KEY")

def search_resort(resort_name):
    """
    Search for snow conditions of a resort.

    Args:
        resort_name (str): The name of the resort to search for.

    Returns:
        dict or None: Dictionary containing snow conditions if found, else None.
    """
    try:
        # Ensure the resort name is not empty
        if not resort_name:
            print("Error: Resort name cannot be empty.")
            return None

        # Encode the resort name for URL
        encoded_resort_name = quote_plus(resort_name)
        url = f"https://ski-resort-forecast.p.rapidapi.com/{encoded_resort_name}/snowConditions"

        # Define headers for API request
        headers = {
            "X-RapidAPI-Key": api_key,  # Use the API key from environment variables
            "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
        }

        # Make a GET request to fetch snow conditions data
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes

        # Parse JSON response
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        # Handle request exception
        print("Error fetching data:", e)
        return None

# Example usage:
if __name__ == "__main__":
    # Define the resort name to search for
    search_value = "YourResortName"
    # Search for snow conditions data of the specified resort
    resort_data = search_resort(search_value)
    if resort_data:
        # Print resort data if found
        print(resort_data)
    else:
        # Notify if no data found for the specified resort
        print("No data found for the specified resort.")
