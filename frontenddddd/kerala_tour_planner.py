import requests
import json

# Function to get user input for days, budget, preferences, and starting location
def get_user_input():
    print("Welcome to the Kerala Tour Planner!")
    place = input("Enter your place of visit (e.g., Kochi): ").strip()
    days = int(input("Enter the number of days for your trip: "))
    budget = float(input("Enter your budget: "))
    preferences = input("Enter your preferences (e.g., beach, adventure, cultural): ").strip().lower()
    return place, days, budget, preferences

# Function to fetch tourist places from Google Maps API
def get_places_from_google_maps(place, preferences, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={preferences}+in+{place}&key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get('results'):
            return data['results']
        else:
            print("Error fetching data from Google Maps or no results found.")
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
        print("Local data file not found.")
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

# Function to display the itinerary
def display_itinerary(itinerary):
    if itinerary:
        print("\nSuggested Itinerary:")
        for idx, item in enumerate(itinerary, start=1):
            print(f"{idx}. {item['name']} - {item['duration']} hours")
    else:
        print("\nNo itinerary could be created for the given duration and preferences.")

# Main function
def main():
    # Google Maps API Key
    api_key = "AIzaSyC0g3bnD3gh9N0esb1iEvL2Lb85a_5r9jc"  # Replace with your actual API key

    # Get user input
    place, days, budget, preferences = get_user_input()

    # Fetch places based on location and preference from Google Maps API
    places = get_places_from_google_maps(place, preferences, api_key)

    # If no results from API, use local data as fallback
    if not places:
        print("\nUsing local data as a fallback...")
        places = get_places_from_local_data(preferences)

    # Generate itinerary based on the number of days
    itinerary = generate_itinerary(places, days)

    # Display the generated itinerary
    display_itinerary(itinerary)

if __name__ == "__main__":
    main()
