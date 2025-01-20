from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Function to fetch tourist places from Google Maps API
def get_places_from_google_maps(place, preferences, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={preferences}+in+{place}&key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get('results'):
            return data['results']
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Google Maps API: {e}")
        return []

# Function to fetch tourist places from a local JSON file as fallback
def get_places_from_local_data(preferences):
    try:
        with open("kerala_tourist_places.json", "r") as file:
            data = json.load(file)
            return [place for place in data if preferences in place['tags']]
    except FileNotFoundError:
        return []

# Function to generate an itinerary based on the number of days
def generate_itinerary(places, days):
    total_hours = days * 8  # Assuming 8 hours per day for activities
    itinerary = []
    for place in places:
        name = place.get('name', 'Unnamed')
        duration = place.get('duration', 2)  # Default duration: 2 hours
        if duration <= total_hours:
            itinerary.append({"name": name, "duration": duration})
            total_hours -= duration
        if total_hours <= 0:
            break
    return itinerary

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary_endpoint():
    data = request.json
    place = data.get('place')
    days = data.get('days', 1)
    budget = data.get('budget', 0)
    preferences = data.get('preferences', '')
    api_key = "AIzaSyC0g3bnD3gh9N0esb1iEvL2Lb85a_5r9jc"  # Replace with a valid API key

    # Fetch places from API or fallback to local data
    places = get_places_from_google_maps(place, preferences, api_key)
    if not places:
        places = get_places_from_local_data(preferences)

    # Generate itinerary based on the number of days
    itinerary = generate_itinerary(places, days)
    return jsonify({"itinerary": itinerary})

if __name__ == "__main__":
    app.run(debug=True)
