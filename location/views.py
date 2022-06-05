from django.shortcuts import render
from .models import Location
import requests
from django.conf import settings
from django.db.models import Count


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
    locations = list(Location.objects.all())
    for locate in locations:
        if address == locate.address:
            lat, lon = (locate.lat, locate.lon)
            return lat, lon
        coordinates = fetch_coordinates(api_key, address)
        if coordinates:
            coordinates_lon, coordinates_lat = coordinates
            return coordinates_lat, coordinates_lon
        return None
