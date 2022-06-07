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


def get_or_create_locations(*addresses):
    api_key = settings.YANDEX_API_KEY
    serialized_addresses = [*addresses]
    locations = {
        locate.address: (locate.lat, locate.lon)
        for locate in Location.objects.filter(address__in=serialized_addresses)
    }
    for address in serialized_addresses:
        if address in [locate for locate in locations.keys()]:
            continue
        coordinates = fetch_coordinates(api_key, address)
        if coordinates:
            coordinates_lon, coordinates_lat = coordinates
            new_locate = Location.objects.create(
                address=address,
                lat=coordinates_lat,
                lon=coordinates_lon,
            )
            locations[new_locate.address] = (new_locate.lat, new_locate.lon)
        else:
            new_locate = Location.objects.create(
                address=address
            )
    return locations

