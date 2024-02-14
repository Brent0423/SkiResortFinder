from flask import Flask, render_template, jsonify, request
from main import fetch_resort_data_sequentially, process_resort_data, sort_resorts
from resorts import resorts
import requests

app = Flask(__name__)

@app.route('/')
def home():
    test_resorts = resorts[:3]
    raw_data = fetch_resort_data_sequentially(test_resorts)
    if raw_data is None:
        return "Error: Unable to fetch resort data", 500
    processed_data = process_resort_data(raw_data)
    if processed_data is None:
        return "Error: Unable to process resort data", 500
    rankings = sort_resorts(processed_data)
    if rankings is None:
        return "Error: Unable to sort resorts", 500
    return render_template('index.html', data=rankings, enumerate=enumerate)

@app.route('/api/resorts')
def resorts_api():
    raw_data = fetch_resort_data_sequentially(resorts[:5])
    if raw_data is None:
        return jsonify([]), 500
    processed_data = process_resort_data(raw_data)
    if processed_data is None:
        return jsonify([]), 500
    sorted_resorts = sort_resorts(processed_data)
    if sorted_resorts is None:
        return jsonify([]), 500
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
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
