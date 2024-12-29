import requests
import json

# Function to get user input for budget, preferences, and starting location (e.g., Kochi)
def get_user_input():
    print("Welcome to the Kerala Tour Planner!")
    place = input("Enter your place of visit (e.g., Kochi): ").strip()
    budget = float(input("Enter your budget: "))
    preferences = input("Enter your preferences (e.g., beach, adventure, cultural): ").strip().lower()
    return place, budget, preferences

# Function to fetch tourist places from Google Maps API based on location and type of preference (e.g., beach, adventure)
def get_places_from_google_maps(place, preferences, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={preferences}+in+{place}&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    # Check if the API returned valid results
    if response.status_code == 200 and data.get('results'):
        return data['results']
    else:
        print("Error fetching data from Google Maps. Please check your API key and internet connection.")
        return []

# Function to filter and recommend places based on budget
def recommend_places(places, budget):
    recommendations = []
    for place in places:
        name = place.get('name')
        address = place.get('formatted_address')
        rating = place.get('rating', "N/A")
        cost_estimate = place.get('price_level', 2)  # Assuming price level from 0 to 4 (0 = cheap, 4 = expensive)
        
        # Assuming cost is represented by price level
        cost = cost_estimate * 200  # Simple estimate: price_level 2 could be around ₹400, price_level 3 ~ ₹600, etc.
        
        if cost <= budget:
            recommendations.append({
                "name": name,
                "address": address,
                "rating": rating,
                "estimated_cost": cost
            })
    
    return recommendations

# Function to display the itinerary
def display_itinerary(recommendations):
    if recommendations:
        print("\nSuggested Tour Itinerary within your budget:")
        for idx, place in enumerate(recommendations, start=1):
            print(f"{idx}. Destination: {place['name']}")
            print(f"   Address: {place['address']}")
            print(f"   Rating: {place['rating']}")
            print(f"   Estimated Cost: ₹{place['estimated_cost']}")
            print("-" * 40)
    else:
        print("\nNo destinations found within your budget and preferences.")

# Main function
def main():
    # Get Google Maps API Key (You need to replace this with your actual key)
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    
    # Get user input
    place, budget, preferences = get_user_input()
    
    # Fetch places based on the location and preference from Google Maps API
    places = get_places_from_google_maps(place, preferences, api_key)
    
    if places:
        # Recommend places based on the budget
        recommendations = recommend_places(places, budget)
        
        # Display the suggested itinerary
        display_itinerary(recommendations)
    else:
        print("\nNo places found based on your preference or there was an error fetching data.")


main()
