# Fetch data from OpenWeather API
import os
import requests
from pprint import pprint

# Introduction message
print("\n💆‍♀️Welcome to the Skincare Recommendation app!💆‍♂️")
print("✨ Please note that these recommendations are general guidelines.")
print("✨ Always listen to your skin and adjust your routine accordingly.\n")

# List of valid skin types
skin_types = ['oily', 'dry', 'combo']

# List of valid country codes
valid_countries = ["US", "GB", "FR", "BE", "ES", "BG", "CZ", "DE", "CA", "AU", "IN", "BR", "JP", "CN"]

# Validate country code from user input
def get_valid_country():
    while True:
        country = input("Enter your country code (e.g., US, GB, FR): ").strip().upper()

        if country in valid_countries:
            print(f"\n✅ You entered a valid country code!")
            return country
        else:
            print("⚠️ Invalid country code. Please enter a **valid two-letter country code** (e.g. US, GB, FR).")

# Ask for skin type input from user
city = input("Enter your city: ").strip().capitalize()
country = get_valid_country()
skin_type = input("Enter your skin type (oily, dry, combo): ").lower().strip()

# Validate city input from user
while not city:
    city = input("Enter your city: ").strip().capitalize()

# Validate  skin type from user input
while skin_type not in skin_types:
    print("⚠️ Invalid choice. Please enter 'oily', 'dry', or 'combo'.")
    skin_type = input("Enter your skin type (oily, dry, combo): ").lower().strip() # Re-prompt the user for a valid input
print(f"\n✅ You selected: {city} city with {skin_type} skin!😊")

# Fetch API key from environment variable
API_KEY = os.getenv("openweather_api_key")
if API_KEY is None:
    print("⚠️ API Key not found! Please set it as an environment variable.")
    exit()

endpoint1 = "https://api.openweathermap.org/data/2.5/weather"

# Setting the parameters for the API
params = {
    "q":f"{city},{country}", # City and country code
    "appid": API_KEY, # API key
    "units":"metric" #convert temp to celcius
}

# API requests
response = requests.get(endpoint1, params=params)

# Check if API request works
if response.status_code == 200:
    weather_data = response.json()
    pprint(weather_data) # API response for debugging

    # Open the file in append mode ("a") so new data is added without deleting old entries
    with open("skincare_recommendations.txt", "a") as file:
        file.write(f"\nCity: {city}\nSkin Type: {skin_type}\n")
        file.write(f"-" * 30 + "\n")

else:
    print("Error: City not found or API request failed. Please check your input.")
    exit() # ✅ Exit if the API call fails

# Extract relevant data from API
temperature = weather_data["main"]["temp"] # Store temp
humidity = weather_data["main"]["humidity"] # Store humidity
wind_speed = weather_data["wind"]["speed"]
weather_condition = weather_data["weather"][0]["description"] # Store weather condition
city_name = weather_data["name"]

# Print extracted values
print(f"\n🌍 City: {city_name}")
print(f"🌡️ Temperature: {temperature}°C")
print(f"💦 Humidity: {humidity}%")
print(f"🌬️ Wind Speed: {wind_speed} m/s")
print(f"☀️ Weather Condition: {weather_condition}")

# Format the extracted data into string
weather_summary = f"""
🌍 City: {city_name}
🌡️ Temperature: {temperature}°C
💦 Humidity: {humidity}%
🌬️ Wind Speed: {wind_speed} m/s
☀️ Weather Condition: {weather_condition}
{"-" * 30}
"""

# Open .txt file in append mode
with open("skincare_recommendations.txt", "a", encoding="utf-8") as file:
    file.write(weather_summary)

# Skincare recommendation based on temperature
def temperature_advice(temperature, skin_type):
    if temperature < 10: # Cold
        if skin_type == "dry":
            return "For dry skin, focus on **intense hydration and barrier repair**. We want nourishing, rich products to lock in moisture and protect against dryness. Use a cream-based cleanser, a hydrating toner for deep moisture, and a thick cream to seal everything in. Look for products with hyaluronic acid and Centella Asisatica."
    elif skin_type == "oily":
        return "For oily skin, focus on **oil control and deep hydration**. Use a foaming cleanser to remove oil without drying the skin, a hydrating toner and a lightweight moisturiser to hydrate the skin without adding extra oil. Cold air can trigger the skin to produce more oil to compensate!"
    else: # Combo skin
        return "For combination skin, focus on **balance and hydration**. You want to use a non-foaming cleanser with a moisturising toner, such as a milky, hydrating toner. Focus on lightweight moisturisers so your pores don't clog up either!"
    return ""

# Skincare recommendation based on humidity
def humidity_advice(humidity, skin_type):
    if humidity > 70:
        if skin_type == "dry":
            return "In humid conditions, if you have dry skin you should be focusing on **hydration and moisture retention**. Use gentle cleansers, followed by alcohol-free hydrating toners and lightweight moisturisers to lock in all that moisture!"
    elif skin_type == "oily":
        return "Focus on **oil control and lightweight hydration** when in humid conditions. Use a foaming cleanser to remove excess oil and a hydrating toner to control shine and tighten your pores. Pair this with an moisturiser that provides hydration but doesn't clog your pores either! This will balance your moisture levels, and keep your skin hydrated without making it greasy!"
    else:
        return "For combination skin in humid weather, the key is **balance and hydration**. Use a gentle cleanser and a hydrating toner, looking for ingredients like ginseng and green tea. This will provide moisture without overloading the oilier areas on your face. Lightweight moisturisers are your friend!"

# Even when no conditions are met, return a string
    return "Adjust your skincare routine according to the humidity levels to maintain balanced skin."


def weather_condition_advice(weather_condition):
    if "rain" in weather_condition.lower() or "wind" in weather_condition.lower():
        return "In windy or rainy conditions, protect your skin barrier with hydration. This means hydrating serums, hydrating moisturisers and hydrating toners! Nothing fights off dull skin like hydration."

    else:
        return "Don't forget SPF, no matter the weather. This is not optional!"

# Store skincare advice
def get_skincare_advice(temperature, humidity, weather_condition, skin_type):
    advice = ""
    advice += temperature_advice(temperature, skin_type)  # Get advice based on temperature
    advice += humidity_advice(humidity, skin_type)  # Get advice based on humidity
    advice += weather_condition_advice(weather_condition)  # Get advice based on weather condition
    return advice

skincare_advice = get_skincare_advice(temperature, humidity, weather_condition, skin_type)

# Print recommendation
print("\n💡 Skincare Recommendation:", skincare_advice)

# Store in .txt file
with open("skincare_recommendations.txt", "a", encoding="utf-8") as file:
    file.write(f"💡 Skincare Advice: {skincare_advice}\n")
    file.write("-" * 30 + "\n")

# Format weather summary to print then store in .txt file
weather_summary_content = (
    f"\nLocation: {city}, {country}\n"
    f"Condition: {weather_condition.capitalize()}\n"
    f"Temperature: {temperature}°C\n"
    f"Humidity: {humidity}%\n"
    f"-" * 30
)

# Store in .txt file
with open("skincare_recommendations.txt", "a") as file:
    file.write(weather_summary_content)

print("\nData successfully stored in 'skincare_recommendations.txt!'")

