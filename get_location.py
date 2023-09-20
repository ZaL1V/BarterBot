import requests


def get_location_by_city(city):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    response = requests.get(url)
    data = response.json()
    lat = data[0].get('lat')
    lon = data[0].get('lon')
    
    return (lat, lon)


def get_location_by_coordinates(lat, lon, language):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language={language}"
    response = requests.get(url)
    data = response.json()

    city = data['address'].get('city') or data['address'].get('town')
    
    return city

