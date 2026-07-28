import requests

def get_coordinates(city):
    try:
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json")
        data = response.json()
        city = data['results'][0]['name']
        country = data['results'][0]['country']
        latitude = data['results'][0]['latitude']
        longitude = data['results'][0]['longitude']
        return city, country, latitude, longitude
    except KeyError:
        print (f"City :{city} has not been correctly spelled")
        return None, None, None, None   

def current_temp(latitude, longitude):
    temp_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m")
    temp_data = temp_response.json()
    temperature = temp_data['current']['temperature_2m']
    return temperature

def get_umbrella(latitude, longitude):
    ppt_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=precipitation_probability")
    ppt_data = ppt_response.json()
    ppt_probability = ppt_data['hourly']['precipitation_probability'][12]
    if ppt_probability > 30:
        return "Get an umbrella!"
    else:
        return "Weather is fine."
    
def weather_brief(city):
    city, country, latitude, longitude = get_coordinates(city)
    if latitude is None:
        print("Could not fetch weather — city not found.")
        return
    temperature = current_temp(latitude, longitude)
    ppt_probability = get_umbrella(latitude, longitude)
    print ("======================")
    print (f"City: {city}, Country: {country}")
    print (f"Temperature: {temperature}")
    print (ppt_probability)
    print (f"Coordinates: {latitude}, {longitude}")

weather_brief("nairobi")
weather_brief("dodoma")
weather_brief("rhjfhj")