from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=200, unique=True, verbose_name='Адрес')
    lat = models.FloatField(null=True, blank=True, verbose_name='Широта')
    lon = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата запроса к геокодеру')

    def __str__(self):
        return f'({self.lon} {self.lat}) {self.address}'

# Create your models here.
