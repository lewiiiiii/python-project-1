import requests
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv("keys.env")
api_key = os.environ.get('api_key')
print(api_key)

def get_coordinates(city):
    try :
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
        data = response.json()
        data.keys()
        city_latitude = data['results'][0]['latitude']
        city_longitude = data['results'][0]['longitude']
        return city_latitude, city_longitude
    except (KeyError, NameError):
        print (f"{city} could not be found")
        return None, None

def current_temp(city_latitude, city_longitude):
    temp_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city_latitude}&longitude={city_longitude}&current=temperature_2m")
    temp_data = temp_response.json()
    temp_data.keys()
    temperature = temp_data['current']['temperature_2m']
    return temperature

def get_umbrella(city_latitude, city_longitude):
    ppt_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city_latitude}&longitude={city_longitude}&hourly=precipitation_probability")
    ppt_data = ppt_response.json()
    ppt_data.keys()
    ppt_data['hourly']['precipitation_probability']
    ppt_probability = ppt_data['hourly']['precipitation_probability'][12]
    print(f"The chance of rain is {ppt_probability}")
    if ppt_probability >= 30:
        return f"Carry an umbrella ({ppt_probability}% chance of rain)"
    else:
        return f"Weather is fine! ({ppt_probability}% chance of rain)"
    

def trending_movie():
    movie_response = requests.get(f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}")
    movie_data = movie_response.json()
    movie_name = movie_data['results'][0]['title']
    movie_popularity = movie_data['results'][0]['popularity']
    return movie_name, movie_popularity

def save_to_csv(city, temperature, umbrella):
    with open('weather_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), city, temperature, umbrella])


def daily_briefing(city):
    city_latitude, city_longitude = get_coordinates(city)
    if city_latitude is None or city_longitude is None:
        print ("could not fetch city")
        return
    temperature = current_temp(city_latitude, city_longitude)
    ppt_probability = get_umbrella(city_latitude, city_longitude)
    movie_name, movie_popularity = trending_movie()
    print(f"===== Daily Briefing for {city} =====")
    print(f"Temperature: {temperature}°C")
    print(f"Umbrella: {ppt_probability}")
    print(f"Trending Movie: {movie_name} (popularity: {movie_popularity})")
    print("=====================================")
    save_to_csv(city, temperature, ppt_probability)

daily_briefing("nairobi")
daily_briefing("mombasa")
daily_briefing("london")
daily_briefing("nyeri")
daily_briefing("berlin")
daily_briefing("ruira")

while True:
    city = input("Enter a city name(or 'quit' to exit):")
    if city.lower() == "quit":
        print ("Goodbye")
        break
    daily_briefing(city)
    