import requests
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv('keys.env')
tmdb_key = os.environ.get('tmdb_key')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
print(client_id)

def get_coordinates(city):
    try :
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
        data = response.json()
        city_latitude = data['results'][0]['latitude']
        city_longitude = data['results'][0]['longitude']
        return city_latitude, city_longitude
    except NameError, KeyError:
        print (f"{city}, could not be found")
        return None, None

def current_temp(city_latitude, city_longitude):
    temp_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city_latitude}&longitude={city_longitude}&current=temperature_2m")
    temp_data = temp_response.json()
    temp_data.keys()
    temperature = temp_data['current']['temperature_2m']
    return temperature

def get_spotify_token():
    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    )
    auth_data = auth_response.json()
    access_token = auth_data['access_token']
    return access_token

def get_mood(temperature):
    if temperature >=30:
        return "amapiano"
    elif temperature >= 25:
        return "afro"
    elif temperature >= 20 :
        return "hiphop"
    else:
        return "house"
    
def search_artist(genre):
    search_response = requests.get(f"https://api.spotify.com/v1/search?q={genre}&type=artist", headers=headers)
    search_data = search_response.json()
    artist_name = search_data['artists']['items'][0]['name']
    return artist_name

def save_to_csv(city, temperature, artist):
    with open("music_weather.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), city, temperature, artist])

def music_weather(city):
    city_latitude, city_longitude = get_coordinates(city)
    if city_latitude is None and city_longitude is None:
        print ("city could not be found")
        return
    temperature = current_temp(city_latitude, city_longitude)
    genre = get_mood(temperature)
    artist_name = search_artist(genre)
    print(f"======Music matcher for {city}=======")
    print(f"Temperature: {temperature}")
    print(f"Mood: {genre}")
    print(f"Top artist: {artist_name}")
    print("===============================")
    save_to_csv(city, temperature, genre)

access_token = get_spotify_token()
headers = {"Authorization": f"Bearer {access_token}"}

music_weather("nairobi")
music_weather("london")
music_weather("seattle")
music_weather("rosario")
music_weather("qatar")
music_weather("ruira")