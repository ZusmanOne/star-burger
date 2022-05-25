from django.shortcuts import render
from .models import Location
import requests
from django.conf import settings


API_KEY = settings.YANDEX_API_KEY


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


def create_locations(address):
    locations = Location.objects.values('address')
    if address in [i['address'] for i in locations]:
        address_location = fetch_coordinates(API_KEY,address)
        if address_location:
            lon, lat = address_location
            return lat, lon
        return None
    else:
        coordinates = fetch_coordinates(API_KEY, address)
        if coordinates:
            coordinates_lon,coordinates_lat = coordinates
            new_location = Location.objects.create(
                address=address,
                lat=coordinates_lat,
                lon=coordinates_lon,
            )
            return new_location.lat, new_location.lon
        else:
            return None
