from django.shortcuts import render
from .models import Location
import requests
from django.conf import settings


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return None
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def create_location(address):
    api_key = settings.YANDEX_API_KEY
    all_location = {locate.address: (locate.lat,locate.lon) for locate in Location.objects.all()}
    if address in all_location:
        lat, lon = all_location[address]
        return lat, lon
    else:
        coordinates = fetch_coordinates(api_key, address)
        if coordinates:
            coordinates_lon, coordinates_lat = coordinates
            return coordinates_lat, coordinates_lon
        else:
            return None
