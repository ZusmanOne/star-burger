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
        all_location[location.address] = (location.lon, location.lat)
    if address not in all_location:
        adr = Location.objects.create(
            address=address,
            lon=fetch_coordinates(API_KEY, address)[0],
            lat=fetch_coordinates(API_KEY, address)[1],

        )
        all_location[adr.address] = (adr.lon, adr.lat)
    return all_location[address]


