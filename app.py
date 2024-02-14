from flask import Flask, render_template, jsonify, request
from main import fetch_resort_data_sequentially, process_resort_data, sort_resorts
from resorts import resorts
import requests  # Ensure this import is present

app = Flask(__name__)

@app.route('/')
def home():
    test_resorts = resorts[:3]  # select the first 3 resorts
    raw_data = fetch_resort_data_sequentially(test_resorts)  # call the function to fetch the raw data
    if raw_data is None:
        print("Error: fetch_resort_data_sequentially returned None")
        raw_data = []
    processed_data = process_resort_data(raw_data)  # process the raw data
    if processed_data is None:
        print("Error: process_resort_data returned None")
        processed_data = []
    rankings = sort_resorts(processed_data)  # get the rankings
    if rankings is None:
        print("Error: sort_resorts returned None")
        rankings = []
    print(rankings)  # print the rankings to the console
    return render_template('index.html', data=rankings, enumerate=enumerate)

@app.route('/api/resorts')
def resorts_api():
    raw_data = fetch_resort_data_sequentially(resorts[:5])
    processed_data = process_resort_data(raw_data)
    sorted_resorts = sort_resorts(processed_data)
    resorts_list = [{'name': name, 'score': score} for name, score in sorted_resorts[:5]]
    return jsonify(resorts_list)

@app.route('/api/search', methods=['GET'])
def search_resort():
    resort = request.args.get('resort', default='Jackson Hole', type=str)
    resort = resort.replace(' ', '%20')
    url = f"https://ski-resort-forecast.p.rapidapi.com/{resort}/snowConditions"
    querystring = {"units": "i"}
    headers = {
        "X-RapidAPI-Key": "e4644d7644mshcb7e90e40cf6593p18d651jsnaf7a44aec097",
        "X-RapidAPI-Host": "ski-resort-forecast.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
