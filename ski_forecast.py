import requests

# Function to fetch forecast data for any resort
def fetch_resort_forecast(resort_name):
    url = f"https://ski-resort-forecast.p.rapidapi.com/{resort_name.replace(' ', '%20')}/snowConditions"

    querystring = {"units":"i","el":"top"}

    headers = {
        "X-RapidAPI-Key": "e4644d7644mshcb7e90e40cf6593p18d651jsnaf7a44aec097",
        "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Example usage
if __name__ == "__main__":
    resort_name = input("Enter the name of the resort: ")
    forecast_data = fetch_resort_forecast(resort_name)
    print(forecast_data)
