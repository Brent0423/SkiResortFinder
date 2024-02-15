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
        if not resort_name:
            print("Error: Resort name cannot be empty.")
            return None

        encoded_resort_name = quote_plus(resort_name)
        url = f"https://ski-resort-forecast.p.rapidapi.com/{encoded_resort_name}/snowConditions"

        headers = {
            "X-RapidAPI-Key": api_key,  # Use the API key from environment variables
            "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None

# Example usage:
if __name__ == "__main__":
    search_value = "YourResortName"
    resort_data = search_resort(search_value)
    if resort_data:
        print(resort_data)
    else:
        print("No data found for the specified resort.")
