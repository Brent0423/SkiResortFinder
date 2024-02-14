import requests
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from 'rapid.env' file
load_dotenv(dotenv_path='rapid.env')

# Access the API_KEY environment variable
api_key = os.getenv("API_KEY")

# Assuming searchValue is obtained securely and sanitized
searchValue = "YourResortName"  # Replace with your logic to obtain the resort name
encoded_searchValue = quote_plus(searchValue)  # URL-encode the search value

url = f"https://ski-resort-forecast.p.rapidapi.com/{encoded_searchValue}/snowConditions"

headers = {
    "X-RapidAPI-Key": api_key,  # Use the API key from environment variables
    "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes
    data = response.json()
    print(data)
    # Handle the data here appropriately
except requests.exceptions.HTTPError as errh:
    print("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("Oops: Something Else", err)
