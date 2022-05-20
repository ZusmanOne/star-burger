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


def create_address(address):
    all_location = {}
    for location in Location.objects.all():
        all_location[location.address] = (location.lat,location.lon)
    if address not in all_location:
        coordinates = fetch_coordinates(API_KEY, address)
        if coordinates:
            adr = Location.objects.create(
                address=address,
                lon=coordinates[1],
                lat=coordinates[0],

            )
        else:
            return None
        all_location[adr.address] = (adr.lon, adr.lat)
    return all_location[address]


