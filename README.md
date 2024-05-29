# Weather App
## Overview
- The Weather App is a Python-based application that allows users to retrieve and display current weather information for a specified city or their current location.
- The app utilizes the OpenWeatherMap API to fetch weather data and uses Tkinter for the graphical user interface.

## Features
- Fetch current weather data by city name or current location.
- Display weather information including temperature, feels like temperature, pressure, humidity, wind speed, and weather description.
- Show weather icons corresponding to the current weather conditions.
- Cache weather data to reduce API calls and improve performance.
- Handle errors gracefully with user-friendly messages.

## Prerequisites
- Python 3.x
- OpenWeatherMap API key

## Installation
1. Clone the Repository:
git clone https://github.com/your-username/weather-app.git
cd weather-app
2. Install Required Libraries:
   - pip install requests geopy
   - pip install from tkinter import
4. Add Your OpenWeatherMap API Key:
- Open weather_app.py and replace "your_actual_api_key" with your actual OpenWeatherMap API key.

## Usage
1. Run the Application:
   python weather_app.py
2. Interact with the App:
- Enter a city name in the text field and press "Search" or hit the Enter key.
- Alternatively, check the "Use my location" option to fetch weather data for your current location.
- The app will display the weather information and corresponding icon.

## File Structure
- weather_app.py: Main application script.
- weather_cache.json: Cache file for storing weather data.

## Contributing
- Contributions are welcome! Please open an issue or submit a pull request with any improvements or features you'd like to add.
