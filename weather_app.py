import requests
import logging
from tkinter import *
from tkinter import messagebox
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import json
import os

# Configuration
API_KEY = "your_actual_api_key"  # Replace with your actual API key
CACHE_FILE = "weather_cache.json"
CACHE_EXPIRY = timedelta(minutes=30)
DEFAULT_CITY = "London"  # Replace with your desired default city

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_weather(city=None, lat=None, lon=None):
    if city:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    else:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data from the weather API: {e}")

    return response.json()

def cache_weather_data(data):
    with open(CACHE_FILE, 'w') as f:
        json.dump({
            "data": data,
            "timestamp": datetime.now().isoformat()
        }, f)

def load_cached_weather_data():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)

    timestamp = datetime.fromisoformat(cache["timestamp"])
    if datetime.now() - timestamp > CACHE_EXPIRY:
        return None

    return cache["data"]

def show_weather():
    try:
        if use_location.get():
            lat, lon = get_location()
            weather_data = get_weather(lat=lat, lon=lon)
        else:
            city = city_entry.get().strip()
            if not city:
                raise ValueError("City name cannot be empty.")
            weather_data = get_weather(city=city)

        cache_weather_data(weather_data)
        update_weather_info(weather_data)
        logging.info(f"Fetched weather data for {weather_data['name']}")
    except ValueError as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", "An error occurred while fetching weather data.")

def update_weather_info(data):
    if data.get('cod') != '404':
        main = data['main']
        wind = data['wind']
        weather = data['weather'][0]
        sys = data['sys']

        temperature = main['temp']
        feels_like = main['feels_like']
        pressure = main['pressure']
        humidity = main['humidity']
        wind_speed = wind['speed']
        description = weather['description']
        country = sys['country']
        city = data['name']
        icon = weather['icon']

        weather_info = (
            f"City: {city}, {country}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Description: {description.capitalize()}"
        )

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/w/{icon}.png"
        response = requests.get(icon_url)
        with open(f"icons/{icon}.png", 'wb') as icon_file:
            icon_file.write(response.content)
        icon_image = PhotoImage(file=f"icons/{icon}.png")
        weather_icon.config(image=icon_image)
        weather_icon.image = icon_image
    else:
        weather_info = "City Not Found!"
        weather_icon.config(image=None)

    weather_label.config(text=weather_info)

def get_location():
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(DEFAULT_CITY)
    return location.latitude, location.longitude

def search_location(event=None):
    show_weather()

app = Tk()
app.title("Weather App")
app.geometry("400x600")
app.resizable(False, False)

use_location = BooleanVar()
location_check = Checkbutton(app, text="Use my location", variable=use_location, font=("Arial", 12))
location_check.pack(pady=10)

city_label = Label(app, text="Enter City Name:", font=("Arial", 12))
city_label.pack(pady=5)

city_entry = Entry(app, width=30, font=("Arial", 12))
city_entry.pack(pady=5)
city_entry.bind("<Return>", search_location)

search_button = Button(app, text="Search", command=show_weather, font=("Arial", 12))
search_button.pack(pady=10)

weather_icon = Label(app)
weather_icon.pack(pady=10)

weather_label = Label(app, text="", font=("Arial", 12), justify=LEFT, anchor="w")
weather_label.pack(pady=20, padx=10)

def check_cache_and_update():
    cached_data = load_cached_weather_data()
    if cached_data:
        logging.info("Using cached weather data")
        update_weather_info(cached_data)
    else:
        logging.info("Fetching fresh weather data")
        show_weather()

check_cache_and_update()
app.mainloop()
