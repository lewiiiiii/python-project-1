import requests
import os
print(os.getcwd())
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv('keys.env')
api_key = os.environ.get("api_key")
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

print(api_key)

def search_movie(title):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}")
        data = response.json()
        movie_name =data['results'][1]['title']
        description = data['results'][1]['overview']
        movie_id = data['results'][1]['id']
        return movie_name, description, movie_id
    except (KeyError, IndexError):
        print (f"Enter a valid movie name. {title} has not been found")
        return None, None, None

def movie_details(movie_id):
    details_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")
    details_data = details_response.json()
    genres = details_data['genres']
    genre_names = []
    for genre in genres:
        genre_names.append(genre['name'])
    first_genre = genre_names[0]
    return genre_names, first_genre

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
    print(auth_data)
    access_token = auth_data['access_token']
    return access_token

def search_artist(first_genre):
    artist_response = requests.get(f"https://api.spotify.com/v1/search?q={first_genre}&type=artist", headers=headers)
    artist_data = artist_response.json()
    artist_name = artist_data['artists']['items'][0]['name']
    return artist_name

def save_to_csv(movie, genre, artist):
    with open("movie_artist_matcher.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), movie, genre, artist])

def movie_artist_matcher(title):
    movie_name, description, movie_id = search_movie(title)
    if movie_id is None:
        print("Could not fetch title")
        return
    genre_names, first_genre = movie_details(movie_id)
    artist_name = search_artist(first_genre)
    print ("==================Movie + Artist Matcher=====================")
    print (f"Movie : {movie_name}")
    print (f"Movie description: {description}")
    print (f"Genres: {genre_names}")
    print (f"Mood genre: {first_genre}")
    print (f"Top artist: {artist_name}")
    print ("--------------------------------------------------------------")
    save_to_csv(movie_name, first_genre, artist_name)

access_token = get_spotify_token()
headers = {"Authorization": f"Bearer {access_token}"}

movie_artist_matcher("sinners")
movie_artist_matcher("f1: the movie")
movie_artist_matcher("jhf")
movie_artist_matcher("el camino")

while True:
    title = input("Enter a movie name or 'quit':")
    if title.lower == "quit":
        print ("Goodbye")
        break
    movie_artist_matcher(title)